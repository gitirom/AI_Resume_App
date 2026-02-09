# --------------------- debug steps --------------------------


# import chonkie
# print(dir(chonkie))

# import chonkie.chunker
# print(dir(chonkie.chunker))

from chonkie import SentenceChunker

chunker = SentenceChunker(chunk_size=400)

print(chunker.chunk("This is a test. This is another sentence."))


