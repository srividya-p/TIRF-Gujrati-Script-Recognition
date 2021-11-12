import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter


def generate(
    text, font, text_color, font_size, orientation, space_width, character_spacing, fit, word_split
):
    if orientation == 0:
        return _generate_horizontal_text(
            text, font, text_color, font_size, space_width, character_spacing, fit, word_split
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(
    text, font, text_color, font_size, space_width, character_spacing, fit, word_split
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_width = int(image_font.getsize(" ")[0] * space_width)

    # These are glyphs that add vowel sounds to consonants. (like 'aa' 'ee' 'uu' etc.)
    # They are represented as ligatures with consonants. 
    # For eg. 'ક (ka)' + 'િ (e)' = 'કિ (ki)'
    vowel_symbols = ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ે', 'ૈ', 'ૃ',  'ૄ', 'ો', 'ૌ', 'ઁ', 'ં', 'ઃ', '્'] 

    # The last character in this list - '્' when present after a consonant, represents a half consonant.
    # They are also represented as ligatures, merged with the following consonant in the word.
    # For eg. 'સ્ (s)' + 'થા (tha)' = 'સ્થા (stha)'

    if word_split:
        # First loop - To split the input text in such a manner that 
        # consonants and vowel symbols come together.
        splitted_text = []
        for word in text.split(' '):
            # Iterate through each character of word
            for i in range(len(word)): 
                # Ignore the character if it is a vowel symbol
                if word[i] in vowel_symbols: continue 
                
                # A consonant was found. Initialise a 'piece' of the splitted list as the first consonant 
                piece, j = word[i], i + 1
                # Keep appending the following characters as long as they are vowel symbols             
                while j < len(word) and word[j] in vowel_symbols: 
                    piece += word[j]
                    j += 1
                
                # Append the piece (consonant + following vowel symbols) to splitted list
                splitted_text.append(piece) 

            # Append space after each word to splitted list
            splitted_text.append(' ') 

        # Remove extra trailing space
        splitted_text.pop()

        # Second loop - Check if there is a half character occourance ('્') 
        # If it is present merge the element with the following element. 
        i, merged_half_chars = 0, []

        while i < len(splitted_text):
            # This element contains a half character
            if '્' in splitted_text[i] and i<len(splitted_text)-1: 
                # Handle case where half character is at the end of the word
                if splitted_text[i + 1] == ' ': 
                    merged_half_chars.append(splitted_text[i])
                # The half character is in between the word
                else:
                    merged_half_chars.append(splitted_text[i]+splitted_text[i + 1]) #Merge the current and next string
                    i += 1
            # This element does not contain half character so just add it to final list
            else: 
                merged_half_chars.append(splitted_text[i])
            i += 1
        splitted_text = merged_half_chars

        # Sample Input for 'text' variable
        # અને ભારતમાં સ્થાન સ્થાનસ્ દૂધની ડેરી કપાસ

        # Sample Output for 'splitted_text' variable
        # ['અ', 'ને', ' ', 'ભા', 'ર', 'ત', 'માં', ' ', 'સ્થા', 'ન', ' ', 'સ્થા', 'ન', 'સ્', ' ', 'દૂ', 'ધ', 'ની', ' ', 'ડે', 'રી', ' ', 'ક', 'પા', 'સ']
    else:
        splitted_text = text

    piece_widths = [image_font.getsize(p)[0] if p != " " else space_width for p in splitted_text]
    text_width = sum(piece_widths)
    if not word_split:
        text_width += character_spacing * (len(text) - 1)

    text_height = max([image_font.getsize(p)[1] for p in splitted_text])

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask, mode="RGB")
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    for i, p in enumerate(splitted_text):
        txt_img_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=fill,
            font=image_font,
        )
        txt_mask_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


def _generate_vertical_text(
    text, font, text_color, font_size, space_width, character_spacing, fit
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask)
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    for i, c in enumerate(text):
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask