require("quirkbase")
math.randomseed(os.time())
math.random()
math.random()
math.random()
-- f2_cap = math.random(0, 5) <= 2 and true or false
f3_cap = math.random(0, 5) <= 2 and true or false
function t1()
    local out = {}
    local cap = str.isupper(input[1])
    for char in list(input) do
        table.insert(out, cap and str.upper(char) or str.lower(char))
        if str.isalpha(char) then cap = not cap end
    end
    return emot.sub(':o)', table.concat(out, ''))
end

function t2()
    local out = {}
    local cap = str.isupper(input[1])
    for char in iter(iterInput) do
        table.insert(out, cap and str.upper(char) or str.lower(char))
        cap = not cap
    end
    return emot.sub(':o)', table.concat(out, ''))
end

function t3()
    f3_cap = not f3_cap
    return emot.sub(':o)', (not f3_cap) and str.upper(input) or str.lower(input))
end

function t4()
    return emot.sub(':o)', str.isupper(input[1]) and str.upper(input) or str.lower(input))
end

-- input = "to jest testowy tekst numer 1 :o)"
-- print(t1())
-- input = "to jest testowy tekst numer 2 :o)"
-- print(t1())
input = "mogę w locie zmienić styl pisania autora"
print(t2())
input = "oraz zapamiętać wartości z poprzednich lini"
print(t2())