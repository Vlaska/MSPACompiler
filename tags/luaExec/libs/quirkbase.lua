table.copy = function(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in next, orig, nil do
            copy[table.copy(orig_key)] = table.copy(orig_value)
        end
        setmetatable(copy, table.copy(getmetatable(orig)))
    else
        -- number, string, boolean, etc
        copy = orig
    end
    return copy
end

table.hasItem = function(tab, val)
    assert(type(tab) == 'table', "tab must be table")

    for _, v in pairs(tab) do
        if v == val then
            return true
        end
    end
    return false
end

table.hasKey = function(tab, val)
    assert(type(tab) == 'table', "tab must be table")

    for k, v in pairs(tab) do
        if k == val then
            return true
        end
    end
    return false
end

def_scope = {
    date = os.date,
    difftime = os.difftime,
    ipairs = ipairs,
    math = math,
    next = next,
    pairs = pairs,
    pcall = pcall,
    print = print,
    select = select,
    string = string,
    table = table,
    time = os.time,
    tonumber = tonumber,
    tostring = tostring,
    type = type,
    utf8 = utf8,
    xpcall = xpcall,

    regex = {}
}

function sethook(func, limit)
    debug.sethook(func, '', limit or 100000000)
end

function removehook()
    debug.sethook()
end

function timeout()
    removehook()
    error('Przekroczono limit maksymalnej liczby lini kodu')
end

function cloneScope(scope)
    if scope then
        return table.copy(scope)
    end
    return table.copy(def_scope)
end

-- function initScope(scope, init)
--     local ret, err = load('function ()' .. init .. '; end', nil, 't', scope)
--     assert(ret, 'Compilation error: ' .. err)
--     ret, err = pcall(ret, nil, 't', scope)
-- end

function compileCode(code, scope)
    assert(type(code) == 'string', 'Code must be a string')
    assert(type(scope) == 'table', 'Scope must be Lua table')

    -- print(code, '\n')

    local ret, err = load('return ' .. code, nil, 't', scope)
    if not ret then
        error('Compilation error: ' .. (err or ''))
    end

    local success, retVal = pcall(ret)
    if not success then
        error('Execution error: ' .. (retVal or ''))
    end

    return function(text, newScope)
        local removehook = removehook
        local sethook = sethook
        local timeout = timeout
        local error = error
        local assert = assert

        local _ENV = newScope and newScope or scope

        output = nil
        sethook(timeout)

        local ok, ret = assert(pcall(retVal, text, arg))
        removehook()

        if ok then
            if ret or output then
                return ret or output
            else
                error('No return value')
            end
        else
            return nil
        end
    end
end
