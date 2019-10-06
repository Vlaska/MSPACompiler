require 'strong'

table.copy = function(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in next, orig, nil do
            copy[table.copy(orig_key)] = table.copy(orig_value)
        end
        setmetatable(copy, table.copy(getmetatable(orig)))
    else -- number, string, boolean, etc
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

    quirks = {}
}

local sethook = function (func, limit)
    debug.sethook(func, '', limit or 1000000)
end

local removehook = function ()
    debug.sethook()
end

local timeout = function ()
    removehook()
    error('Przekroczono limit maksymalnej liczby lini kodu')
end

function cloneScope()
    return table.copy(def_scope)
end

function callFunction(scope, funcIndex, lineLimit)
    local funcIndexType = type(funcIndex)

    local removehook = removehook
    local sethook = sethook
    local timeout = timeout
    local error = error
    local assert = assert
    
    local _ENV = scope
    
    if funcIndexType == nil then
        for k, _ in pairs(quirks) do
            funcIndex = k
            break
        end
        
        if not funcIndex then
            error("No function to call")
        end
    elseif table.hasItem({'number', 'string'}, type(funcIndex)) then
        --print(funcIndex, quirks[funcIndex])
        assert(table.hasKey(quirks, funcIndex), 'No function with given name')
    else
        error('FuncIndex is required')
    end


    output = nil
    sethook(timeout)
    
    local ok, ret = assert(pcall(quirks[funcIndex]))
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

function register(content, scope, name)
    assert(type(content) == 'string', 'Content must be a string')
    assert(type(scope) == 'table', 'Scope must be Lua table')
    assert(type(name) == 'string', 'Name must be a string')
    local ret, err = load(content, nil, 't', scope)
    assert(ret, 'Compilation error: %s' % err)
    if name == 'vars' then
        local ok, ret = pcall(ret)
    else
        scope[name] = ret
    end
end

function compileQuirk(func, scope, index)
    assert(type(func) == 'string', 'func must be a string')
    assert(type(scope) == 'table', 'Scope must be Lua table')
    
    local ret, err = load('return %s' % func, nil, 't', scope)
    assert(ret, 'Compilation error: %s' % err)
    
    local ok, func = pcall(ret)
    assert(ok, 'Execution error: %s' % func)
    table.insert(scope.quirks, index or (#scope.quirks + 1), func)
    
    return scope
end

function sandbox(inputText, scope, funcIndex, lineLimit)
    assert(inputText and type(inputText == 'string'), 'No text to parse provided or incorrect type')
    assert(scope and type(scope) == 'table', 'Incorrect scope')
    if lineLimit then
        assert(type(lineLimit) == 'number', 'Line limit must be a number')
    end

    scope.input = inputText

    local out = callFunction(scope, funcIndex, lineLimit)
    scope.input = nil

    return out
end