#!/usr/bin/python
#author: Bryan Bishop <kanzure@gmail.com>
#date: 2012-01-02
#purpose: compute full map pointers
import json

#parse hex values as base 16 (see calculate_pointer)
base = 16

#where to load the rom from
rom_filename = "../baserom.gbc"
rom = None #load the rom later

#map header pointers start at 0x1AE
start_map_header_pointers = 0x1AE

#bank bytes for each map header start at 0xC23D
start_map_header_pointer_banks = 0xC23D

#number of maps in this list
map_count = 0xF8 #including the 0th the total is is 248 or 0xF8

maps = {
         0x00: "Pallet Town",
         0x01: "Viridian City",
         0x02: "Pewter City",
         0x03: "Cerulean City",
         0x04: "Lavendar Town", #??
         0x05: "Vermilion City", #correct
         0x06: "Celadon City",
         0x07: "Fuchsia City",
         0x08: "Cinnabar Island",
         0x09: "Indigo Plateau",
         0x0A: "Saffron City",
         0x0B: "FREEZE",
         0x0C: "Route 1",
         0x0D: "Route 2",
         0x0E: "Route 3",
         0x0F: "Route 4",
         0x10: "Route 5",
         0x11: "Route 6",
         0x12: "Route 7",
         0x13: "Route 8",
         0x14: "Route 9",
         0x15: "Route 10",
         0x16: "Route 11",
         0x17: "Route 12",
         0x18: "Route 13",
         0x19: "Route 14",
         0x1A: "Route 15",
         0x1B: "Route 16",
         0x1C: "Route 17",
         0x1D: "Route 18",
         0x1E: "Route 19",
         0x1F: "Route 20",
         0x20: "Route 21",
         0x21: "Route 22",
         0x22: "Route 23",
         0x23: "Route 24",
         0x24: "Route 25",
         0x25: "Ash's House F1",
         0x26: "Ash's House F2",
         0x27: "Gary's House",
         0x28: "Oak's Lab",
         0x29: "Viridian Poke Center",
         0x2A: "Viridian Mart",
         0x2B: "School",
         0x2C: "Viridian House",
         0x2D: "Viridian Gym",
         0x2E: "Digletts Cave (Route 2)",
         0x2F: "Viridian Forest (exit)",
         0x30: "Route 2 House",
         0x31: "Route 2 Gate",
         0x32: "Viridian Forest (Entrance)",
         0x33: "Viridian Forest",
         0x34: "Museum F1",
         0x35: "Museum F2",
         0x36: "Pewter Gym",
         0x37: "Pewter House (1)",
         0x38: "Pewter Mart",
         0x39: "Pewter House (2)",
         0x3A: "Pewter PokeCenter",
         0x3B: "Mt. Moon (1)",
         0x3C: "Mt. Moon (2)",
         0x3D: "Mt. Moon (3)",
         0x3E: "Cerulean House (Trashed)",
         0x3F: "Cerulean House (2)",
         0x40: "Cerulean Pokecenter",
         0x41: "Cerulean Gym",
         0x42: "Bike Shop",
         0x43: "Cerulean Mart",
         0x44: "Mt. Moon Pokecenter",
         0x45: "COPY OF: Trashed House",
         0x46: "Route 5 Gate",
         0x47: "Underground Tunnel Entrance (Route 5)",
         0x48: "Day Care M",
         0x49: "Route 6 Gate",
         0x4A: "Underground Tunnel Entrance (Route 6)",
         0x4B: "COPY OF: Underground Tunnel Entrance (Route 6)",
         0x4C: "Route 7 Gate",
         0x4D: "Underground Path Entrance (Route 7)",
         0x4E: "COPY OF: Underground Path Entrance (Route 7)",
         0x4F: "Route 8 Gate",
         0x50: "Underground Path Entrance (Route 8)",
         0x51: "Rock Tunnel Pokecenter",
         0x52: "Rock Tunnel (1)",
         0x53: "Power Plant",
         0x54: "Route 11 Gate",
         0x55: "Digletts Cave Entrance (Route 11)",
         0x56: "Route 11 Gate (Upstairs)",
         0x57: "Route 12 Gate",
         0x58: "Bill's House",
         0x59: "Vermilion PokeCenter",
         0x5A: "Fan Club",
         0x5B: "Vermilion Mart",
         0x5C: "Vermilion Gym",
         0x5D: "Vermilion House (1)",
         0x5E: "Vermilion Dock",
         0x5F: "S.S. Anne (1)",
         0x60: "S.S. Anne (2)",
         0x61: "S.S. Anne (3)",
         0x62: "S.S. Anne (4)",
         0x63: "S.S. Anne (5)",
         0x64: "S.S. Anne (6)",
         0x65: "S.S. Anne (7)",
         0x66: "S.S. Anne (8)",
         0x67: "S.S. Anne (9)",
         0x68: "S.S. Anne (10)",
         0x69: "FREEZE",
         0x6A: "FREEZE",
         0x6B: "FREEZE",
         0x6C: "Victory Road (1)",
         0x6D: "FREEZE",
         0x6E: "FREEZE",
         0x6F: "FREEZE",
         0x70: "FREEZE",
         0x71: "Lance",
         0x72: "FREEZE",
         0x73: "FREEZE",
         0x74: "FREEZE",
         0x75: "FREEZE",
         0x76: "Hall of Fame Room",
         0x77: "Underground Path (N/S)",
         0x78: "Gary",
         0x79: "Underground Path (W/E)",
         0x7A: "Celadon Mart (1)",
         0x7B: "Celadon Mart (2)",
         0x7C: "Celadon Mart (3)",
         0x7D: "Celadon Mart (4)",
         0x7E: "Celadon Mart (5)",
         0x7F: "Celadon Mart (6)",
         0x80: "Celadon Mansion (1)",
         0x81: "Celadon Mansion (2)",
         0x82: "Celadon Mansion (3)",
         0x83: "Celadon Mansion (4)",
         0x84: "Celadon Mansion (5)",
         0x85: "Celadon Pokecenter",
         0x86: "Celadon GYM",
         0x87: "Celadon Game Corner",
         0x88: "Celadon House",
         0x89: "Celadon Prize Room",
         0x8A: "Celadon Diner",
         0x8B: "Celadon House (2)",
         0x8C: "Celadon Hotel",
         0x8D: "Lavender Pokecenter",
         0x8E: "Pokemon Tower (1)",
         0x8F: "Pokemon Tower (2)",
         0x90: "Pokemon Tower (3)",
         0x91: "Pokemon Tower (4)",
         0x92: "Pokemon Tower (5)",
         0x93: "Pokemon Tower (6) ",
         0x94: "Pokemon Tower (7)",
         0x95: "Lavender House (1)",
         0x96: "Lavender Mart",
         0x97: "Lavender House (2)",
         0x98: "Fuchsia Mart",
         0x99: "Fuchsia House (1)",
         0x9A: "Fuchsia Pokecenter",
         0x9B: "Fuchsia House (2)",
         0x9C: "Safari Zone Entrance",
         0x9D: "Fuchsia GYM",
         0x9E: "Fuchsia Meeting Room",
         0x9F: "Seafoam Islands (2)",
         0xA0: "Seafoam Islands (3)",
         0xA1: "Seafoam Islands (4)",
         0xA2: "Seafoam Islands (5)",
         0xA3: "Vermilion House (2)",
         0xA4: "Fuchsia House (3)",
         0xA5: "Mansion (1)",
         0xA6: "Cinnibar Gym",
         0xA7: "Lab (1)",
         0xA8: "Lab (2)",
         0xA9: "Lab (3)",
         0xAA: "Lab (4)",
         0xAB: "Cinnibar Pokecenter",
         0xAC: "Cinnibar Mart",
         0xAD: "COPY: Cinnibar Mart",
         0xAE: "Indigo Plateau Lobby",
         0xAF: "Copycat's House F1",
         0xB0: "Copycat's House F2",
         0xB1: "Fighting Dojo",
         0xB2: "Saffron Gym",
         0xB3: "Saffron House (1)",
         0xB4: "Saffron Mart",
         0xB5: "Silph Co (1)",
         0xB6: "Saffron Pokecenter",
         0xB7: "Saffron House (2)",
         0xB8: "Route 15 Gate",
         0xBA: "Route 16 Gate Map",
         0xBB: "Route 16 Gate Upstairs",
         0xBC: "Route 16 House",
         0xBD: "Route 12 House",
         0xBE: "Route 18 Gate",
         0xBF: "Route 18 Gate Header",
         0xC0: "Seafoam Islands (1)",
         0xC1: "Route 22 Gate",
         0xC2: "Victory Road (2)",
         0xC3: "Route 12 Gate Upstairs",
         0xC4: "Vermilion House (3)",
         0xC5: "Diglett's Cave",
         0xC6: "Victory Road (3)",
         0xC7: "Rocket Hideout (1)",
         0xC8: "Rocket Hideout (2)",
         0xC9: "Rocket Hideout (3)",
         0xCA: "Rocket Hideout (4) ",
         0xCB: "Rocket Hideout (Elevator)",
         0xCC: "FREEZE",
         0xCD: "FREEZE",
         0xCE: "FREEZE",
         0xCF: "Silph Co (2)",
         0xD0: "Silph Co (3)",
         0xD1: "Silph Co (4)",
         0xD2: "Silph Co (5)",
         0xD3: "Silph Co (6)",
         0xD4: "Silph Co (7)",
         0xD5: "Silph Co (8)",
         0xD6: "Mansion (2)",
         0xD7: "Mansion (3)",
         0xD8: "Mansion (4)",
         0xD9: "Safari Zone East",
         0xDA: "Safari Zone North",
         0xDB: "Safari Zone West",
         0xDC: "Safari Zone Center",
         0xDD: "Safari Zone Rest House (1)",
         0xDE: "Safari Zone Secret House",
         0xDF: "Safari Zone Rest House (2)",
         0xE0: "Safari Zone Rest House (3)",
         0xE1: "Safari Zone Rest House (4)",
         0xE2: "Unknown Dungeon (2)",
         0xE3: "Unknown Dungeon (3)",
         0xE4: "Unknown Dungeon (1)",
         0xE5: "Name Rater",
         0xE6: "Cerulean House (3)",
         0xE7: "FREEZE",
         0xE8: "Rock Tunnel (2)",
         0xE9: "Silph Co (9)",
         0xEA: "Silph Co (10)",
         0xEB: "Silph Co (11)",
         0xEC: "Silph Co (Elevator)",
         0xED: "FREEZE",
         0xEE: "FREEZE",
         0xEF: "Battle Center M",
         0xF0: "Trade Center M",
         0xF1: "FREEZE",
         0xF2: "FREEZE",
         0xF3: "FREEZE",
         0xF4: "FREEZE",
         0xF5: "Loreli",
         0xF6: "Bruno",
         0xF7: "Agatha"
       }

map_pointers = {
    #0x00: {
    #       "name": "Pallet Town",
    #       "address": 0x182a1
    #      },
               }

map_headers = {
    #0x00: {
    #       "name": "Pallet Town",
    #       "address": 0x182a1,
    #       "tileset"
    #       "y"
    #       "x"
    #       "map_pointer"
    #       "texts_pointer"
    #       "script_pointer"
    #       "connection_byte"
    #       "num_connections"
    #       "connections":
    #        { "0":
    #          { map_id, connected_map_tile_pointer, current_map_tile_pointer, bigness, width, y, x, window_pointer }
    #        },
    #       "object_data_pointer"
    #      },
              }

#haters gonna hate
def load_rom(filename=None):
    "load the rom into a global (returns True/False)"
    global rom

    if not filename:
        filename = rom_filename

    try:
        rom = open(filename, "rb").read()
        return True
    except Exception, exception:
        print "error loading rom"
        return False

def assert_rom():
    global rom
    assert rom, "rom must be loaded, see load_rom()"

def calculate_pointer(short_pointer, bank):
    short_pointer = int(short_pointer)
    bank = int(bank)

    pointer = short_pointer - 0x4000 + (bank * 0x4000)

    #result will be an integer
    return pointer

def get_nth_map_header_pointer_bank_byte_address(map_id):
    "returns the address to the bank byte associated with this map pointer"
    address = start_map_header_pointer_banks + map_id
    return address

def get_nth_map_header_pointer_bank_byte(map_id):
    "returns the bank number for this map header"
    assert_rom()

    address = get_nth_map_header_pointer_bank_byte_address(map_id)
    bank_byte = ord(rom[address])
    return bank_byte

def get_nth_map_header_pointer(map_id):
    "returns the full pointer to the map header struct for this map"
    assert_rom()

    #figure out where the bytes for this pointer are located
    byte1_address = start_map_header_pointers + (map_id * 2)
    byte2_address = start_map_header_pointers + (map_id * 2) + 1

    #grab the two bytes making up the partial pointer
    byte1 = ord(rom[byte1_address])
    byte2 = ord(rom[byte2_address])

    #swap the bytes (16-bit pointers for z80 are little endian)
    temp = byte1
    byte1 = byte2
    byte2 = temp
    del temp

    #combine these into a single pointer (0x byte1 byte2)
    partial_pointer = (byte2 + (byte1 << 8))
    #print hex(partial_pointer)

    #get the bank id
    bank = get_nth_map_header_pointer_bank_byte(map_id)

    #calculate the full pointer
    pointer = calculate_pointer(partial_pointer, bank)

    #return it as an integer
    return pointer

def load_map_pointers():
    global maps
    global map_pointers

    for map in maps.keys():
        pointer = get_nth_map_header_pointer(map)
        #print maps[map] + "\t\t\t" + hex(pointer)

        entry = {
                "name": maps[map],
                "address": hex(pointer),
                "bank": hex(get_nth_map_header_pointer_bank_byte(map))
                }
        map_pointers[map] = entry
    
    #print json.dumps(map_pointers)

def read_connection_bytes(connection_bytes, bank):
    map_id = ord(connection_bytes[0])
    
    #connection strip
    connected_map_tile_pointer_byte1 = ord(connection_bytes[1])
    connected_map_tile_pointer_byte2 = ord(connection_bytes[2])
    connected_map_tile_pointer = (connected_map_tile_pointer_byte1 + (connected_map_tile_pointer_byte2 << 8))

    #connection strip
    current_map_tile_pointer_byte1 = ord(connection_bytes[3])
    current_map_tile_pointer_byte2 = ord(connection_bytes[4])
    current_map_tile_pointer = (current_map_tile_pointer_byte1 + (current_map_tile_pointer_byte2 << 8))

    bigness_byte = ord(connection_bytes[5])
    width_byte = ord(connection_bytes[6])
    y = ord(connection_bytes[7])
    x = ord(connection_bytes[8])

    #window
    window_pointer_byte1 = ord(connection_bytes[9])
    window_pointer_byte2 = ord(connection_bytes[10])
    window_pointer = (window_pointer_byte1 + (window_pointer_byte2 << 8))

    connection_data = {
                      "map_id": map_id,
                      "connected_map_tile_pointer": hex(connected_map_tile_pointer),
                      "current_map_tile_pointer": hex(current_map_tile_pointer),
                      "bigness": hex(bigness_byte),
                      "width": hex(width_byte),
                      "y": y,
                      "x": x,
                      "window_pointer": hex(window_pointer),
                      }
    return connection_data

def read_map_header(address, bank): #bank because i'm lazy
    address = int(address, base)
    bank = int(bank, base)

    tileset = ord(rom[address])
    y = ord(rom[address+1])
    x = ord(rom[address+2])

    map_pointer_byte1 = ord(rom[address+3])
    map_pointer_byte2 = ord(rom[address+4])
    partial_map_pointer = (map_pointer_byte1 + (map_pointer_byte2 << 8))
    map_pointer = calculate_pointer(partial_map_pointer, bank)

    texts_pointer_byte1 = ord(rom[address+5])
    texts_pointer_byte2 = ord(rom[address+6])
    partial_texts_pointer = (texts_pointer_byte1 + (texts_pointer_byte2 << 8))
    texts_pointer = calculate_pointer(partial_texts_pointer, bank)

    script_pointer_byte1 = ord(rom[address+7])
    script_pointer_byte2 = ord(rom[address+8])
    partial_script_pointer = (script_pointer_byte1 + ( script_pointer_byte2 << 8))
    script_pointer = calculate_pointer(partial_script_pointer, bank)

    connection_byte = ord(rom[address+9]) #0xc = NORTH | SOUTH
    # <&IIMarckus> the connection byte is a bitmask allowing 0-4 connections
    # <&IIMarckus> each connection is 11 bytes
    # <&IIMarckus> or'd
    # <&IIMarckus> east = 1, west = 2, south = 4, north = 8
    # <&IIMarckus> so a connection byte of 0xc means north/south
    # <&IIMarckus> which means there are 22 more bytes, 11 for each connection
    # < kanzure> 4 | 8 = c?
    # <&IIMarckus> yes
    # <&IIMarckus> easier to see if you convert to binary
    # <&IIMarckus> 0100 | 1000 = 1100

    num_connections = 0
    connection_value = bin(connection_byte)[2:]
    if connection_value[0] == "1": #NORTH
        num_connections += 1
    if len(connection_value) > 1 and connection_value[1] == "1": #SOUTH
        num_connections += 1
    if len(connection_value) > 2 and connection_value[2] == "1": #WEST
        num_connections += 1
    if len(connection_value) > 3 and connection_value[3] == "1": #EAST
        num_connections += 1
 
    #quick test for connection data
    #connection0_stuff = rom[(address + 10):(address + 10 + 11)]
    #print "Route: " + hex(ord(connection0_stuff[0]))

    #setup
    connections = {}

    #go straight to object data if there are no connections
    if num_connections > 0:
        for connection in range(0, num_connections):
            base_connection_address = address + 10 + (11 * connection)
            connection_bytes = rom[base_connection_address : base_connection_address + 11]
            connection_data = read_connection_bytes(connection_bytes, bank)

            connections[connection] = connection_data

    #we might have to jump around a bit
    offset = address + 10 + (11 * num_connections)

    #object data
    object_data_pointer_byte1 = ord(rom[offset])
    object_data_pointer_byte2 = ord(rom[offset+1])
    partial_object_data_pointer = (object_data_pointer_byte1 + (object_data_pointer_byte2 << 8))
    object_data_pointer = calculate_pointer(partial_object_data_pointer, bank)

    map_header = {
                 "tileset": hex(tileset),
                 "y": hex(y),
                 "x": hex(x),
                 "map_pointer": hex(map_pointer),
                 "texts_pointer": hex(texts_pointer),
                 "script_pointer": hex(script_pointer),
                 "connection_byte": hex(connection_byte),
                 "num_connections": str(num_connections),
                 "connections": connections, #NORTH, SOUTH, WEST, EAST order matters
                 "object_data_pointer": hex(object_data_pointer),
                 }
    return map_header

def read_all_map_headers():
    if rom == None: load_rom()
    assert_rom()
    if len(map_pointers) == 0: load_map_pointers()

    for map_id in map_pointers.keys():
        map = map_pointers[map_id]
        map_header = read_map_header(map["address"], map["bank"])

        map_header["id"] = map_id
        map_header["name"] = map["name"]
        map_header["address"] = map["address"]
        map_header["bank"] = map["bank"]

        map_headers[map_id] = map_header
    
    return map_headers

if __name__ == "__main__":
    #read binary data from file
    load_rom()
    
    #where are the map structs?
    load_map_pointers()
    #print json.dumps(map_pointers)

    #experimental...
    #print json.dumps(read_map_header(map_pointers[0]["address"], map_pointers[0]["bank"]))

    read_all_map_headers()
    print json.dumps(map_headers)
