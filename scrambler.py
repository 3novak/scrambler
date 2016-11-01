# scramble information
# since the scrambler and turbulator don't interact at all, the order
# of functions in reversing the scrambling are commutative and associative.

import copy


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def chunker(txt):
    enc = bin(int.from_bytes(txt.encode(), 'big'))[2:]
    enc = '0' + enc
    chunks = [enc[i:i+8] for i in range(0, len(enc), 8)]
    return chunks


def chunk_bits(bits):
    enc = '0' + bits
    chunks = [enc[i:i+8] for i in range(0, len(enc), 8)]
    return chunks


def scrambler(chunks):
    # vulnerability is the handling (lack thereof) in the last chunks for
    # lists of length not divisible by three.
    #print('length:', len(chunks), '\nrange_length:', 3 * int(len(chunks) / 3))
    new = copy.deepcopy(chunks)
    for chunk_ix in range(0, 3 * int(len(new) / 3)):
        new[chunk_ix] = chunks[chunk_ix + 1 - 3*int((chunk_ix + 1)/3) + 3*int(chunk_ix/3)]
    return new


def unscrambler(chunks):
    # undoes the scrambler action
    # applied to chunks already individually in order
    return scrambler(scrambler(chunks))


def turbulator(bits):
    # applied to individual chunks
    # the turbulator has order 2, so just apply to the turbulated form
    # to unturbulate the string
    tmp = [0]*len(bits)
    # switch_plan is totally arbitrary
    switch_plan = {0: 2, 1: 4, 2: 0, 3: 3, 4: 1, 5: 7, 6: 6, 7: 5}
    for ix in range(0, len(tmp)):
        tmp[ix] = bits[switch_plan[ix]]
    turbulated = ''.join(tmp)
    return turbulated


def master_scrambler(original_txt):
    round1 = chunker(original_txt)
    round2 = scrambler(round1)
    round3 = [None]*len(round2)
    for ix in range(0, len(round2)):
        round3[ix] = turbulator(round2[ix])
    encoded_bytes = ''.join(round3)
    encoded_bytes = encoded_bytes[1:]
    return encoded_bytes


def master_decoder(scrambled_txt):
    round1 = chunk_bits(scrambled_txt)
    round2 = [None]*len(round1)
    for ix in range(0, len(round1)):
        round2[ix] = turbulator(round1[ix])
    round3 = unscrambler(round2)
    round4 = ''.join(round3)
    round4 = round4[1:]
    txt = text_from_bits(round4)
    return txt


if __name__ == '__main__':
    route_txt = input('scramble or unscramble?\n')
    if 'un' in route_txt:
        init_txt = input('input some bytes to unscramble!\n')
        print(master_decoder(init_txt))
    else:
        init_txt = input('input some text to scramble!\n')
        print(master_scrambler(init_txt))
