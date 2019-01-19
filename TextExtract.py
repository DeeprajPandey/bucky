import io
import time
from google.cloud import videointelligence_v1p2beta1 as videointelligence

print('Hello!')

def jw_distance(sherlock, watson):
    sherlock_len = len(sherlock)
    watson_len = len(watson)
    
    if not sherlock_len or not watson_len:
        return 0.0
    
    # According to Jaro similarity, 2 characters are matching
    # only if they are same and in the range defined below in `search_range`
    min_len = max(sherlock_len, watson_len)
    search_range = (min_len // 2) - 1
    # Negative search_range was a bug for hours. Ugh.
    if search_range < 0:
        search_range = 0

    # Array of flags corresponding to each character, which will toggle to True
    # when they match b/w the strings
    sherlock_flags = [False]*sherlock_len
    watson_flags = [False]*watson_len


    # While searching only within the search_range, count & flag matched pairs
    common_chars = 0
    for i, sherlock_ch in enumerate(sherlock):
        low = i - search_range if i > search_range else 0
        hi = i + search_range if i + search_range < watson_len else watson_len - 1
        for j in range(low, hi+1):
            # if flag has been toggled to True, we continue
            if not watson_flags[j] and watson[j] == sherlock_ch:
                sherlock_flags[i] = watson_flags[j] = True
                common_chars += 1
                # If a common character is found, again
                # compare the next character in sherlock with the range in watson
                break

    # If no characters match, m=0
    if not common_chars:
        return 0.0
    
    # Count transpositions
    # Note: only check order of matched characters.
    # For instance, DwAyNE and DuANE have 0 transpositions since the
    # matching letters (range-wise as well) D,A,N,E are in same order.
    k = trans_count = 0
    for i, sherlock_f in enumerate(sherlock_flags):
        if sherlock_f:
            for j in range(k, watson_len):
                if watson_flags[j]:
                    k = j + 1
                    break
            # Means matching but at different positions
            if sherlock[i] != watson[j]:
                trans_count += 1
    # We counted once for each character in sherlock.
    # If transpositions exist, they're counted twice
    trans_count /= 2
    
    # Adjust for similarities in nonmatched characters
    common_chars = float(common_chars)
    # Jaro Distance
    weight = ((common_chars/sherlock_len + common_chars/watson_len +
               (common_chars-trans_count) / common_chars)) / 3
        
    # Winkler modification: continue to boost if strings are similar
    if weight > 0.7 and sherlock_len > 3 and watson_len > 3:
        # adjust for up to first 4 chars in common
        j = min(min_len, 4)
        i = 0
        while i < j and sherlock[i] == watson[i] and sherlock[i]:
            i += 1
            if i:
                # The scaling factor, p, is usually 0.1
                weight += i * 0.15 * (1.0 - weight)
    return weight


video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.TEXT_DETECTION]
video_context = videointelligence.types.VideoContext()

with io.open("uploads/userVid.mov", 'rb') as file:
   input_content = file.read()

# input_uri='gs://bucky_video_repo/progressive_writing.mov'

operation = video_client.annotate_video(
    input_content=input_content,  # the bytes of the video file
    features=features,
    video_context=video_context)

print('Processing video for text detection.')
prev_time = time.time()
result = operation.result(timeout=3000)
curr_time = time.time() 
print('Process Time: ' + str(curr_time - prev_time))

prev_time = curr_time

# The first result is retrieved because a single video was processed.
annotation_result = result.annotation_results[0]

#f = open("output.txt", "w")
#f.write(str(annotation_result))

dict = {}
for textAnnotation in  annotation_result.text_annotations:
    key = textAnnotation.segments[0].segment.start_time_offset.seconds + (textAnnotation.segments[0].segment.start_time_offset.nanos * 1e-9)
    dict[key] = textAnnotation.text

lines = []
keys = sorted(dict)
for key in keys:
    lines.append(dict[key])
#    print(str(key) + ': ' + dict[key])

curr_time = time.time() 
print('Traversal Time: ' + str(curr_time - prev_time))

prev_time = curr_time

code = []
for line in lines:
    lineNo = len(code)
    if lineNo == 0:
        code.append(line)
    else:
        distance = jw_distance(code[lineNo - 1], line)
#        print(str(distance) + ' : ' + code[lineNo - 1] + ' : ' + line)
        if distance >= 0.75:
            code[lineNo - 1] = line
        else:
            code.append(line)

#print("No of lines: " + str(len(code)))
source_code = '';
for line in code:
    source_code += line
    source_code += '\n'

f = open("SourceCode.txt", "w")
f.write(source_code)

curr_time = time.time() 
print('Tuning Time: ' + str(curr_time - prev_time))
