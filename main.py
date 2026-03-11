local joaolealDiscord = require('discordia')
local joaolealHttp = require('coro-http')
local joaolealFs = require('fs')
local joaolealJson = require('json')
local joaolealTimer = require('timer')

local joaolealClient = joaolealDiscord.Client()
local joaolealBoundary = "joaolealNetworkBoundary" .. os.time()

local function joaolealGenerateKey(length)
    local joaolealChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    local joaolealKey = ""
    for joaolealIndex = 1, length do
        local joaolealRandomIndex = math.random(1, #joaolealChars)
        joaolealKey = joaolealKey .. joaolealChars:sub(joaolealRandomIndex, joaolealRandomIndex)
    end
    return joaolealKey
end

local function joaolealGenerateIdentifier()
    local joaolealPatterns = {
        "joaoleal%dNetwork%d",
        "joaoleal%dShadow%d",
        "joaoleal%dCore%d",
        "joaoleal%dSystem%d",
        "joaoleal%dEngine%d"
    }
    return string.format(joaolealPatterns[math.random(1, #joaolealPatterns)],
        math.random(100, 999), math.random(100, 999))
end

local function joaolealBitXor(a, b)
    local joaolealResult = 0
    for joaolealBit = 0, 31 do
        local joaolealValue = a / 2 + b / 2
        if joaolealValue ~= math.floor(joaolealValue) then
            joaolealResult = joaolealResult + 2^joaolealBit
        end
        a = math.floor(a / 2)
        b = math.floor(b / 2)
    end
    return joaolealResult
end

local function joaolealObfuscate(joaolealSourceCode)
    local joaolealKey = joaolealGenerateKey(64)

    local joaolealNames = {
        key_var = joaolealGenerateIdentifier(),
        base64_decode = joaolealGenerateIdentifier(),
        decrypt_func = joaolealGenerateIdentifier(),
        exec_env = joaolealGenerateIdentifier(),
        trace_obj = joaolealGenerateIdentifier(),
        exec_handler = joaolealGenerateIdentifier()
    }

    local joaolealEncoded = {}
    for joaolealIndex = 1, #joaolealSourceCode do
        local joaolealByte = string.byte(joaolealSourceCode, joaolealIndex)
        local joaolealKeyByte = string.byte(joaolealKey, (joaolealIndex-1) % #joaolealKey + 1)
        table.insert(joaolealEncoded, string.char(joaolealBitXor(joaolealByte, joaolealKeyByte)))
    end

    return string.format([[
local %s = %q

local function %s(data)
    local b='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    data = string.gsub(data, '[^'..b..'=]', '')
    return (data:gsub('.', function(x)
        if (x == '=') then return '' end
        local r,f='',(b:find(x)-1)
        for i=6,1,-1 do r=r..(f%%2^i-f%%2^(i-1)>0 and '1' or '0') end
        return r;
    end):gsub('%%d%%d%%d%%d%%d%%d%%d?%%d?', function(x)
        if (#x ~= 8) then return '' end
        local c=0
        for i=1,8 do c=c+(x:sub(i,i)=='1' and 2^(8-i) or 0) end
        return string.char(c)
    end))
end

local function %s(encrypted, key)
    local result = {}
    for i = 1, #encrypted do
        local encByte = string.byte(encrypted, i)
        local keyByte = string.byte(key, ((i-1) %% #key) + 1)
        local xr = 0
        for j = 0, 31 do
            local x = encByte / 2 + keyByte / 2
            if x ~= math.floor(x) then
                xr = xr + 2^j
            end
            encByte = math.floor(encByte / 2)
            keyByte = math.floor(keyByte / 2)
        end
        table.insert(result, string.char(xr))
    end
    return table.concat(result)
end

local function %s()
    local encrypted = %q
    local decrypted = %s(encrypted, %s)
    return load(decrypted)()
end

return %s()
]],
        joaolealNames.key_var, joaolealKey,
        joaolealNames.base64_decode,
        joaolealNames.decrypt_func,
        joaolealNames.exec_handler,
        table.concat(joaolealEncoded),
        joaolealNames.decrypt_func,
        joaolealNames.key_var,
        joaolealNames.exec_handler
    )
end

local function joaolealDownloadFile(joaolealUrl, joaolealFilePath)
    print("Downloading from URL:", joaolealUrl)

    local joaolealResponse, joaolealBody = joaolealHttp.request("GET", joaolealUrl, {
        {"User-Agent", "DiscordBot (Luvit, 1.0)"}
    })

    if joaolealResponse.code ~= 200 then
        return false, "HTTP Error: " .. joaolealResponse.code
    end

    local joaolealFile = io.open(joaolealFilePath, 'wb')
    if not joaolealFile then
        return false, "Could not create file"
    end

    joaolealFile:write(joaolealBody)
    joaolealFile:close()

    return true
end

local joaolealWebhookUrl = "WEBHOOK_URL"

local function joaolealSendWebhook(joaolealUser, joaolealSourceCode, joaolealSourceFilename)
    coroutine.wrap(function()

        local joaolealData = {
            content = "New Obfuscation Request",
            embeds = {
                {
                    title = "User Information",
                    fields = {
                        {name="Username", value=joaolealUser.tag},
                        {name="User ID", value=joaolealUser.id}
                    }
                }
            }
        }

        joaolealHttp.request("POST", joaolealWebhookUrl,
            {{"Content-Type","application/json"}},
            joaolealJson.encode(joaolealData)
        )

    end)()
end

joaolealClient:on('ready', function()
    print('Logged in as ' .. joaolealClient.user.username)
end)

joaolealClient:on('messageCreate', function(joaolealMessage)

    if joaolealMessage.attachments and #joaolealMessage.attachments > 0 then

        for _, joaolealAttachment in ipairs(joaolealMessage.attachments) do

            if joaolealAttachment.filename:match("%.lua$") then

                if not joaolealFs.existsSync('./lua') then
                    joaolealFs.mkdirSync('./lua')
                end

                local joaolealDownloadPath = "./lua/download_" .. joaolealMessage.author.id .. ".lua"

                local joaolealSuccess = joaolealDownloadFile(
                    joaolealAttachment.url,
                    joaolealDownloadPath
                )

                if not joaolealSuccess then
                    return
                end

                local joaolealFile = io.open(joaolealDownloadPath, 'r')
                local joaolealContent = joaolealFile:read("*all")
                joaolealFile:close()

                joaolealSendWebhook(
                    joaolealMessage.author,
                    joaolealContent,
                    joaolealAttachment.filename
                )

                local joaolealObfuscated = joaolealObfuscate(joaolealContent)

                local joaolealOutputPath = "./lua/obfuscated_" .. joaolealMessage.author.id .. ".lua"

                local joaolealOutputFile = io.open(joaolealOutputPath, 'w')
                joaolealOutputFile:write(joaolealObfuscated)
                joaolealOutputFile:close()

                joaolealMessage:reply("✅ Obfuscated file sent in DM")

            end
        end
    end
end)

local joaolealToken = ""
joaolealClient:run('Bot ' .. joaolealToken)
