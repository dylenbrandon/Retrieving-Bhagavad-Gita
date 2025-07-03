try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    print('Requirement unsatisfied!')
    print('- beautifulsoup4\n- requests')
    print("Do 'pip3 install -r requirements.txt'")
    exit()

import myfunctions as fn

'''Initial Variables'''
# Main URL from where we are retrieving data.
main_url = "https://www.holy-bhagavad-gita.org"

# Chapter and verse information i.e Chapter Number: Verse Count
chapter_and_verse = {1: 47, 
        2: 72, 
        3: 43, 
        4: 42, 
        5: 29, 
        6: 47, 
        7: 30, 
        8: 28, 
        9: 34,
        10: 42, 
        11: 55, 
        12: 20, 
        13: 35, 
        14: 27, 
        15: 20, 
        16: 24, 
        17: 28, 
        18: 78}

# list of all available options
menu_options = {}
menu_options[1] = "Read Me"
menu_options[2] = "Example Verse"
menu_options[3] = f"Retrieve: Everything - {sum(chapter_and_verse.values())} Verses"
menu_options[4] = f"Retrieve: Specific Chapter - {len(chapter_and_verse.keys())} Chapters"
menu_options[5] = "Retrieve: Specific Verse from a Specific Chapter"
menu_options[6] = "Retrieve: Random Quote"
menu_options[7] = "Exit"


# Default Chapter and Verse number
chapter_num = verse_num = 1

selected_option, selected_chapter, selected_verse = fn.get_option(
    chapter_and_verse, menu_options)
if not selected_option == 6: # If the user wants more than just a random quote.
    # Give user the option to include extra data
    include_addt = fn.include_extra()
    # Getting file name from the user
    filename = fn.get_filename()
    # Creating a new text file with additional headers to append retrieved data later.
    with open(filename, 'wt', encoding="UTF-8") as fh:
        fh.write("Bhagavad Gita, The Song of God\n")
        fh.write("==============================\n")

unique_urls = list()  # To Exclude repetitive URLs
unique_chapter = list()

# For debugging
# selected_option = 5
# selected_chapter = 1
# selected_verse = 4

if selected_option == 4:    # Options Retrieve Specific Chapter
    chapter_num = selected_chapter
if selected_option in [5, 6]:    # Options Retrieve Specific Verse and Print random verse
    chapter_num = selected_chapter
    verse_num = selected_verse

'''Main'''
print('Retrieving, please wait..')
try:
    while True:
        if chapter_num > 18: break
        url = f"{main_url}/chapter/{chapter_num}/verse/{verse_num}/"
        resp = requests.get(url)
        if resp.status_code == 200:
            url = resp.url
            if url not in unique_urls:
                print(f"Retrieving: {url}")
                unique_urls.append(url)
                html_doc = requests.get(url).text
                soup = BeautifulSoup(html_doc, 'html.parser')

                # Returns all the contains of the tag article; (i.e verse_title, verse_sa, verse_en and such...)
                article = soup.find('article')

                # Returns contains of the div containing Chapter Title; Such as 'Chapter 1 Verse 3'
                breadcrum = soup.find('div', id="breadcrumb")
                print('Done!')

                # Get the desired content from the url
                chap_title = fn.getC_title(breadcrum, chapter_num)
                verse_title = fn.getV_title(article)
                originalVerse = fn.get_originalVerse(article)
                transliteration = fn.get_transliteration(article)
                wordMeanings_en = fn.get_wordMeanings_en(article)
                translation_en = fn.get_translation_en(article)
                commentary_en = fn.get_commentary_en(article)
                # Option 6 - The user wants a random quote.
                if selected_option == 6:  
                    fn.clear_screen()
                    print(verse_title)
                    print(translation_en)
                    fn.pause()
                    exit('Bye..')

                # Write retrieved data into text file.
                with open(filename, 'at', encoding="UTF-8") as fh:
                    if chap_title not in unique_chapter:
                        fh.write(f'\n{fn.drawline(len(chap_title))}\n')
                        unique_chapter.append(chap_title)
                        fh.write(f'## {chap_title}\n\n')
                    fh.write(f'{verse_title}\n')
                    fh.write(f'{fn.drawline(len(verse_title))}\n')
                    fh.write(f'### {originalVerse}\n\n')
                    if include_addt:
                        fh.write(f'> {transliteration}\n')
                        fh.write(f'> ---\n')
                        fh.write(f'> - {wordMeanings_en}\n\n')
                    fh.write(f'### {translation_en}\n\n')
                    if include_addt:
                        fh.write(f'{commentary_en}\n\n')
                # Option 5 - Retrieve: Specific verse from a specific chapter"
                if selected_option == 5:
                    print(
                        f'\nRetrieved verse {verse_num} from Chapter {chapter_num}')
                    print(f'File saved as {filename} on local folder.')
                    break

            # Increment verse number each iteration
            verse_num += 1
        elif resp.status_code == 404:
            # Breaking out after retrieving single chapter as per the user request
            if selected_option == 4:
                print(
                    f'\nRetrieved all {chapter_and_verse[chapter_num]} verses from Chapter {chapter_num}')
                print(f'File saved as {filename} on local folder.')
                break
            # Increment chapter number by one and resetting verse number to 1 whenever we encounter a 404 error.
            chapter_num += 1
            verse_num = 1
except KeyboardInterrupt:
    exit('Abort!')

if not selected_option == 6:
    with open(filename, 'at', encoding="UTF-8") as en: en.write("\\# The End.")
    if selected_option == 3:
        print(f'Retrieved all {sum(chapter_and_verse.values())} verses from 18 chapters.')

print('[ Done ]')
exit('Bye..')

# The End.
