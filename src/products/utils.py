import logging

from django.utils.text import slugify


def format_text(text_to_modify):

    text_to_modify = " " + text_to_modify.lower() + " "
    # Remove unwanted words
    text_to_modify = (text_to_modify
        .replace(" au ", " ")
        .replace(" à ", " ")
        .replace(" a ", " ")
        .replace(" la ", " ")
        .replace(" le ", " ")
        .replace(" aux ", " ")
        .replace(" en ", " ")
        .replace(" et ", " ")
        .replace(" de ", " ")
        .replace(" des ", " ")
        .replace(" du ", " ")
        .replace(" marque: ", " ")
        .replace(" marque ", " ")
        .replace(" marques: ", " ")
        .replace(" marques ", " ")
        .replace(" brands: ", " ")
        .replace(" brands ", " ")
        .replace(" code: ", " ")
    )

    text_to_modify = (text_to_modify
        .replace(" & ", " et ")
        .replace("&", " et "))

    text_to_modify = text_to_modify.replace(".", "xxpoointxx")
    text_to_modify = text_to_modify.replace(",", "xxviirgxx")
    text_to_modify = slugify(text_to_modify).replace("-", " ")
    text_to_modify = text_to_modify.replace("xxpoointxx", ".")
    text_to_modify = text_to_modify.replace("xxviirgxx", ",")
    return format_quantity_and_unit(text_to_modify)
    


def format_quantity_and_unit(text_to_modify):
    """Format quantity.
    - Turn 1000 ml into 1l
    - Turn 1,5 L into 1.5l
    """

    if not isinstance(text_to_modify,str):
        logging.error("Error! Text to modify is not a string")
        return ""

    text_to_modify = remove_space_between_quantity_and_unit(text_to_modify)
    text_to_modify = (text_to_modify
        .replace(" 0,5l", " 50cl")
        .replace(" 0.5l", " 50cl")
        .replace(" 1,5l", " 1.5l")
        .replace(" 1,25l", " 1.25l")
        .replace(" 2,5l", " 2.5l")
        .replace(" 0.75l", " 75cl")
        .replace(" 0,75l", " 75cl")
        .replace(" 0.33l", " 33cl")
        .replace(" 0,33l", " 33cl")
        .replace(" 250ml", " 25cl")
        .replace(" 330ml", " 33cl")
        .replace(" 500ml", " 50cl")
        .replace(" 600ml", " 60cl")
        .replace(" 750ml", " 75cl")
        .replace(" 1000ml", " 1l")
        .replace(" 1500ml", " 1.5l")
        .replace(" 0.2kg", " 200g")
        .replace(" 0,2kg", " 200g")
        .replace(" 0.3kg", " 300g")
        .replace(" 0,3kg", " 300g")
        .replace(" 0.5kg", " 500g")
        .replace(" 0,5kg", " 500g")
        .replace(" 0.75kg", " 750g")
        .replace(" 0,75kg", " 750g")
        .replace(" gramme ", "g ")
        .replace(" grammes ", "g ")
        .replace(" grame ", "g ")
        .replace(" grames ", "g ")
        .replace(" gram ", "g ")
        .replace(" grams ", "g ")
        .replace(" litre ", "l ")
        .replace(" litres ", "l ")
        .replace(" kilogramme ", "kg ")
        .replace(" kilogrammes ", "kg ")
        .replace(" kilogrames ", "kg ")
        .replace(" kilogrammes ", "kg ")
        .replace(" liter ", "l ")
        .replace(" liters ", "l ")
    )
    return text_to_modify


def remove_space_between_quantity_and_unit(text_to_modify):
    text_to_modify = text_to_modify.strip()
    text_to_modify = " " + text_to_modify + " "
    return (text_to_modify
            .replace(" l ", "l ")
            .replace(" cl ", "cl ")
            .replace(" ml ", "ml ")
            .replace(" hl ", "hl ")
            .replace(" dl ", "dl ")
            .replace(" g ", "g ")
            .replace(" kg ", "kg ")
            .replace(" Kg ", "Kg ")
            .replace(" mm ", "mm ")
            .replace(" cm ", "cm ")
            .replace(" dm ", "dm ")
            .replace(" m2 ", "m2 ")
            .replace(" m² ", "m² ")
            .replace(" m3 ", "m3 ")
            .replace(" m³ ", "m³ ")
            .replace(" cm2 ", "cm2 ")
            .replace(" cm² ", "cm² ")
            .replace(" cm3 ", "cm3 ")
            .replace(" cm³ ", "cm³ ")
            .replace(" mm2 ", "mm2 ")
            .replace(" mm² ", "mm² ")
            .replace(" mm3 ", "mm3 ")
            .replace(" mm³ ", "mm³ "))