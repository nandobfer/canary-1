function Player:getRace()
    local race
    local player = self:getPlayer()
    local resultId = db.storeQuery('SELECT race FROM players WHERE name = ' .. db.escapeString(player:getName()))
    if resultId then
        race = result.getNumber(resultId, "race")
    end
    result.free(resultId)
    return race
end

function raceStartUp(player)
    local races = {
        [0] = humanStartUp,
        [1] = elfStartUp,
        [2] = goblinStartUp,
        [3] = orcStartUp,
        [4] = dwarfStartUp,
    }
    local index = player:getRace()
    races[index](player)
end


function Player:setRaceSkin()
    player = self:getPlayer()
    local race = player:getRace()
    if race == 0 then
        return false
    end
    local skins = {
        [0] = {
            [0] = "none",
            [1] = "sorcerer",
            [2] = "druid",
            [3] = "paladin",
            [4] = "knight",
            [9] = "assassin",
            [10] = "necromancer",
            [11] = "hunter",
        },
        [1] = {
            [0] = "elf",
            [1] = "elf arcanist",
            [2] = "elf",
            [3] = "elf",
            [4] = "elf",
            [9] = "elf",
            [10] = "elf arcanist",
            [11] = "elf scout",
        },
        [2] = {
            [0] = "goblin",
            [1] = "goblin",
            [2] = "goblin",
            [3] = "goblin scavenger",
            [4] = "goblin scavenger",
            [9] = "goblin assassin",
            [10] = "goblin",
            [11] = "goblin",
        },
        [3] = {
            [0] = "orc",
            [1] = "orc shaman",
            [2] = "orc spearman",
            [3] = "orc warrior",
            [4] = "orc warlord",
            [9] = "orc leader",
            [10] = "orc shaman",
            [11] = "orc spearman",
        },
        [4] = {
            [0] = "dwarf",
            [1] = "dwarf geomancer",
            [2] = "dwarf geomancer",
            [3] = "dwarf guard",
            [4] = "dwarf guard",
            [9] = "dwarf soldier",
            [10] = "dwarf geomancer",
            [11] = "dwarf",
        },
    }
    local skin = Condition(CONDITION_OUTFIT)
    skin:setTicks(-1)
    skin:setOutfit(MonsterType(skins[race][player:getVocation():getId()]):getOutfit())
    player:addCondition(skin)
end


function raceTown(player)
    local town
    if player:getRace() == 0 then
        town = Town(8) -- Thais
    elseif player:getRace() == 1 then
        town = Town(5) -- Ab'Dendriel
    elseif player:getRace() == 2 then
        town = Town(6) -- Carlin
    elseif player:getRace() == 3 then
        town = Town(13) -- Darashia
    elseif player:getRace() == 4 then
        town = Town(7) -- Kazordoon
    else
        town = Town(8) -- Thais
    end

    player:teleportTo(town:getTemplePosition())
    player:setTown(town)

end

----------- HUMAN -----------

function humanStartUp(player)
    if player:getStorageValue(Storage_.race) ~= 0 then
        return false
    end

end

----------- ELF -----------

function elfStartUp(player)
    -- Elf LookType
    player:setRaceSkin()

    -- Elf distance fightning bonus
    local archer = Condition(CONDITION_ATTRIBUTES)
    local distance = player:getSkillLevel(SKILL_DISTANCE)
    archer:setTicks(-1)
    archer:setParameter(CONDITION_PARAM_SKILL_DISTANCE, 10)
    player:addCondition(archer)
end
----------- GOBLIN -----------

function goblinStartUp(player)

    -- Goblin LookType
    player:setRaceSkin()
end

----------- ORC

function orcStartUp(player)

    -- Orc LookType
    player:setRaceSkin()
end

----------- DWARF

function dwarfStartUp(player)

    -- Dwarf LookType
    player:setRaceSkin()
end