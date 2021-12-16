import math


class Packet:
    def __init__(self, version, type, subpackets, literal):
        self.version = version
        self.type = type
        self.subpackets = subpackets
        self.literal = literal

    @property
    def version_sum(self):
        return self.version + sum(sub.version_sum for sub in self.subpackets)

    @property
    def value(self):
        match self.type:
            case 0:
                return sum(sub.value for sub in self.subpackets)
            case 1:
                return math.prod(sub.value for sub in self.subpackets)
            case 2:
                return min(sub.value for sub in self.subpackets)
            case 3:
                return max(sub.value for sub in self.subpackets)
            case 4:
                return self.literal
            case 5:
                return 1 if self.subpackets[0].value > self.subpackets[1].value else 0
            case 6:
                return 1 if self.subpackets[0].value < self.subpackets[1].value else 0
            case 7:
                return 1 if self.subpackets[0].value == self.subpackets[1].value else 0
            case _:
                raise Exception(f"unhandled type: {self.type}")

    def print(self, indent=""):
        type_specific = ""
        if self.type == 4:
            type_specific = f" Literal: {self.literal}"
        else:
            type_specific = f" Subpackets: {len(self.subpackets)}"

        print(f"{indent}Version: {self.version} Type: {self.type}{type_specific}")
        for n in range(len(self.subpackets)):
            print(f"{indent}  - Subpacket {n}:")
            self.subpackets[n].print(indent + "    ")


def parse_packet(bits):
    version = int(bits[:3], 2)
    _type = int(bits[3:6], 2)
    bits = bits[6:]

    if _type == 4:
        # Literal packet
        literal = 0
        done = False
        while not done:
            done = bits[0] == "0"
            lb, bits = int(bits[1:5], 2), bits[5:]
            literal = (literal << 4) + lb
        return Packet(version, _type, [], literal), bits
    else:
        # Operator packet
        length_type = "bits" if bits[0] == "0" else "packets"
        length_bit_count = 15 if length_type == "bits" else 11
        length_bits, bits = bits[1 : length_bit_count + 1], bits[length_bit_count + 1 :]
        length = int(length_bits, 2)
        subpackets = []

        if length_type == "bits":
            sub_bits, bits = bits[:length], bits[length:]
            while sub_bits:
                subpacket, sub_bits = parse_packet(sub_bits)
                subpackets.append(subpacket)
        elif length_type == "packets":
            for _ in range(length):
                subpacket, bits = parse_packet(bits)
                subpackets.append(subpacket)

        return Packet(version, _type, subpackets, None), bits


with open("input.txt") as f:
    data = f.read().strip()

bits = "".join([f"{int(h, 16):04b}" for h in data])
pkt, _ = parse_packet(bits)

print(f"Part 1: {pkt.version_sum}")
print(f"Part 2: {pkt.value}")
