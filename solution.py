from pprint import pprint
import sys

# Method Definitions
def processPhotos(line, id):
    photo = {}
    line = line.split(" ")
    photo['id'] = id
    photo['orientation'] = line[0]
    photo['num_tags'] = int(line[1])
    photo['tags'] = []
    for n in range(0, photo['num_tags']):
        photo['tags'].append(line[n+2])

    return photo

def processFile(file):
    with open(file, 'r') as inp:
        numPhotos = int(inp.readline())
        photos = {}
        most_tags = [-1, -1]
        for n in range(0, numPhotos):
            photos[n] = processPhotos(inp.readline()[:-1], n)
            if photos[n]['num_tags'] > most_tags[1]:
                most_tags[0] = n
                most_tags[1] = photos[n]['num_tags']

        photos['metadata'] = {'most_tags': most_tags[0]}
        #pprint(photos)

    return photos

def findMatch(tags, photos, vertical = False):
    done = False
    best_match = [-1, -1]
    #print('search')
    for next_id in photos:
        photo_next = photos[next_id]
        if next_id == 'metadata':
            continue
        if vertical and photo_next['orientation'] != 'V':
            continue
        #pprint(photo_next)
        next_tags = photo_next['tags']
        match = 0
        for tag in next_tags:
            if tag in tags:
                match += 1
        interest = min(match, len(next_tags)-match, len(tags)-match)

        if interest > best_match[1]:
            best_match[0] = next_id
            best_match[1] = interest

        #least_tags = 0
        #if len(tags) > len(next_tags):
        #    least_tags = len(next_tags)
        #else:
        #    least_tags = len(tags)
        #if best_match[1] >= least_tags:
        #    break

    #print(best_match[0])
    if best_match[0] == -1:
        return None, done

    if best_match[1] == 0:
        done = True


    return photos[best_match[0]], done



def createSlideShow(photos):
    slideshow = []
    S = photos['metadata']['most_tags']
    S = photos[S]
    done = False
    while not done and len(photos) > 1:
        print(len(photos), end='\r')
        del photos[S['id']]
        slide = ''
        if S['orientation'] == 'H':
            tags = S['tags']
            Sn, done = findMatch(tags, photos)
            slide = S['id']
        else:
            tags = S['tags']
            Sn, done = findMatch(tags, photos, True)
            #print(Sn)
            del photos[Sn['id']]
            tags = list(set(tags + Sn['tags']))
            slide = "{} {}".format(S['id'], Sn['id'])
            Sn, done = findMatch(tags, photos)


        slideshow.append(slide)
        S = Sn
        if S is None:
            break

    return slideshow

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        file_path = input_file.split('\\')
        file_name = input_file[len(input_file)-1]
    else:
        input_file = 'a_example.txt'
    output = ".\\Solutions\\solution_{}.txt".format(file_name[0])
    print(output)
    photos = processFile(input_file)
    slideshow = createSlideShow(photos)
    with open(output, 'w') as output:
        print(len(slideshow), file=output)
        for slide in slideshow:
            print(slide, file=output)
        print('Done')
