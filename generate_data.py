import json
import random
from typing import List, Tuple

# Templates and variations for noisy STT patterns
FIRST_NAMES = [
    "ramesh", "priyanka", "rohan", "meera", "arjun", "kavya", "vikram", "ananya",
    "suresh", "deepika", "raj", "neha", "amit", "pooja", "rahul", "sonia",
    "kiran", "divya", "manoj", "swati", "naveen", "ritu", "sanjay", "priya"
]

LAST_NAMES = [
    "sharma", "verma", "mehta", "patel", "kumar", "singh", "reddy", "nair",
    "desai", "jain", "gupta", "rao", "iyer", "menon", "kapoor", "malhotra"
]

EMAIL_DOMAINS = [
    "gmail", "yahoo", "outlook", "hotmail", "rediffmail", "icloud", "protonmail"
]

CITIES = [
    "mumbai", "delhi", "bangalore", "chennai", "hyderabad", "pune", "kolkata",
    "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur", "indore", "thane",
    "bhopal", "visakhapatnam", "patna", "vadodara", "ghaziabad", "ludhiana"
]

LOCATIONS = [
    "airport", "hospital", "school", "college", "mall", "park", "station",
    "restaurant", "hotel", "office", "bank", "library", "museum", "theater"
]

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

# Number word mappings for noisy STT
NUMBER_WORDS = {
    "0": ["zero", "oh", "o"],
    "1": ["one"],
    "2": ["two"],
    "3": ["three"],
    "4": ["four"],
    "5": ["five"],
    "6": ["six"],
    "7": ["seven"],
    "8": ["eight"],
    "9": ["nine"]
}


def number_to_words(digits: str, prob_spell: float = 0.4) -> str:
    """Convert digits to spelled-out words with some probability"""
    result = []
    for digit in digits:
        if random.random() < prob_spell and digit in NUMBER_WORDS:
            result.append(random.choice(NUMBER_WORDS[digit]))
        else:
            result.append(digit)
    if len(result) > 1 and any(len(r) > 1 for r in result):
        return " ".join(result)
    return "".join(result)


def generate_credit_card() -> str:
    """Generate credit card number in various formats"""
    formats = [
        lambda: f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
        lambda: f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}",
        lambda: number_to_words(str(random.randint(1000, 9999))) + " " + 
                str(random.randint(1000, 9999)) + " " + 
                str(random.randint(1000, 9999)) + " " + 
                str(random.randint(1000, 9999)),
    ]
    return random.choice(formats)()


def generate_phone() -> str:
    """Generate phone number in various formats"""
    formats = [
        lambda: str(random.randint(9000000000, 9999999999)),
        lambda: f"{random.randint(90, 99)} {random.randint(10000000, 99999999)}",
        lambda: " ".join([number_to_words(str(random.randint(0, 9)), prob_spell=0.6) for _ in range(10)]),
        lambda: number_to_words(str(random.randint(90, 99)), prob_spell=0.5) + " " + 
                number_to_words(str(random.randint(10000000, 99999999)), prob_spell=0.3),
    ]
    return random.choice(formats)()


def generate_email() -> str:
    """Generate email in STT format"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    domain = random.choice(EMAIL_DOMAINS)
    
    formats = [
        f"{first} dot {last} at {domain} dot com",
        f"{first} {last} at {domain} dot com",
        f"{first} dot {last} at {domain} com",
        f"{first} underscore {last} at {domain} dot com",
    ]
    return random.choice(formats)


def generate_person_name() -> str:
    """Generate person name"""
    formats = [
        lambda: random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
        lambda: random.choice(FIRST_NAMES),
        lambda: random.choice(LAST_NAMES),
    ]
    return random.choice(formats)()


def generate_date() -> str:
    """Generate date in various formats"""
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(2020, 2025)
    
    formats = [
        lambda: f"{day:02d} {month:02d} {year}",
        lambda: f"{day} {month} {year}",
        lambda: f"{day} {MONTHS[month-1]} {year}",
        lambda: f"{number_to_words(str(day), prob_spell=0.3)} {number_to_words(str(month), prob_spell=0.3)} {year}",
    ]
    return random.choice(formats)()


def generate_example(num_entities: int = None) -> dict:
    """Generate a single training example"""
    if num_entities is None:
        num_entities = random.randint(1, 4)
    
    # Build text incrementally to track offsets correctly
    text_parts = []
    entities = []
    current_pos = 0
    
    # Generate intro phrases
    intros = [
        "hi", "hello", "i need", "please", "can you", "i want", "my", "the",
        "i am", "call me", "reach me", "contact me", "email me", "send to",
        "i", "this is"
    ]
    
    # Add random intro
    if random.random() < 0.8:
        intro = random.choice(intros)
        text_parts.append(intro)
        current_pos += len(intro)
        if text_parts:  # Add space if not first
            current_pos += 1
    
    # Generate entities
    entity_types = ["CREDIT_CARD", "PHONE", "EMAIL", "PERSON_NAME", "DATE", "CITY", "LOCATION"]
    selected_types = random.sample(entity_types, min(num_entities, len(entity_types)))
    
    connectors = ["is", "are", "and", "also", "plus", "with", "or"]
    
    for i, entity_type in enumerate(selected_types):
        # Add connector
        if i > 0 or (i == 0 and text_parts):
            connector = random.choice(connectors)
            text_parts.append(connector)
            current_pos += len(connector) + 1
        
        # Generate entity and prefix
        entity_text = None
        prefix = None
        
        if entity_type == "CREDIT_CARD":
            entity_text = generate_credit_card()
            prefix = random.choice(["credit card", "card number", "card", "credit card number"])
        elif entity_type == "PHONE":
            entity_text = generate_phone()
            prefix = random.choice(["phone", "number", "mobile", "contact", "phone number"])
        elif entity_type == "EMAIL":
            entity_text = generate_email()
            prefix = random.choice(["email", "email id", "mail", "email address"])
        elif entity_type == "PERSON_NAME":
            entity_text = generate_person_name()
            if random.random() < 0.3:
                prefix = random.choice(["name", "i am", "this is"])
        elif entity_type == "DATE":
            entity_text = generate_date()
            if random.random() < 0.6:
                prefix = random.choice(["on", "date", "by", "from"])
        elif entity_type == "CITY":
            entity_text = random.choice(CITIES)
            if random.random() < 0.5:
                prefix = random.choice(["in", "from", "at"])
        elif entity_type == "LOCATION":
            entity_text = random.choice(LOCATIONS)
            if random.random() < 0.5:
                prefix = random.choice(["at", "in", "near", "to"])
        
        # Add prefix if exists
        if prefix:
            text_parts.append(prefix)
            current_pos += len(prefix) + 1
        
        # Calculate entity position
        entity_start = current_pos
        
        # Add entity
        text_parts.append(entity_text)
        entity_end = entity_start + len(entity_text)
        current_pos = entity_end + 1
        
        # Store entity
        entities.append({
            "start": entity_start,
            "end": entity_end,
            "label": entity_type
        })
    
    # Join text parts with spaces
    text = " ".join(text_parts)
    
    # Verify and fix entity positions (they might be off by spaces)
    entities_fixed = []
    for entity in entities:
        # Find the entity text in the actual text
        label = entity["label"]
        # The entity text should be in text_parts, find its actual position
        entity_text = None
        for part in text_parts:
            if label == "CREDIT_CARD" and any(c.isdigit() for c in part) and len(part.replace(" ", "")) >= 12:
                entity_text = part
                break
            elif label == "PHONE" and any(c.isdigit() for c in part) and len(part.replace(" ", "")) == 10:
                entity_text = part
                break
            elif label == "EMAIL" and "at" in part and "dot" in part:
                entity_text = part
                break
            elif label == "PERSON_NAME" and (part in FIRST_NAMES or part in LAST_NAMES or " " in part and any(n in part for n in FIRST_NAMES + LAST_NAMES)):
                entity_text = part
                break
            elif label == "DATE" and (any(c.isdigit() for c in part) or any(m in part for m in MONTHS)):
                entity_text = part
                break
            elif label == "CITY" and part in CITIES:
                entity_text = part
                break
            elif label == "LOCATION" and part in LOCATIONS:
                entity_text = part
                break
        
        if entity_text:
            # Find actual position in text
            start = text.find(entity_text)
            if start != -1:
                end = start + len(entity_text)
                entities_fixed.append({
                    "start": start,
                    "end": end,
                    "label": label
                })
    
    # Sort entities by start position
    entities_fixed.sort(key=lambda x: x["start"])
    
    return {
        "text": text,
        "entities": entities_fixed
    }


def main():
    random.seed(42)  # For reproducibility
    
    # Generate training data (500-1000 examples)
    train_count = random.randint(500, 1000)
    print(f"Generating {train_count} training examples...")
    
    train_data = []
    for i in range(train_count):
        example = generate_example()
        train_data.append({
            "id": f"utt_{i+1:04d}",
            "text": example["text"],
            "entities": example["entities"]
        })
        if (i + 1) % 100 == 0:
            print(f"  Generated {i+1}/{train_count} examples...")
    
    # Write training data
    with open("data/train.jsonl", "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"Generated {len(train_data)} training examples")
    
    # Generate dev data (100-200 examples)
    dev_count = random.randint(100, 200)
    print(f"Generating {dev_count} dev examples...")
    
    dev_data = []
    for i in range(dev_count):
        example = generate_example()
        dev_data.append({
            "id": f"utt_{i+1:04d}",
            "text": example["text"],
            "entities": example["entities"]
        })
        if (i + 1) % 50 == 0:
            print(f"  Generated {i+1}/{dev_count} examples...")
    
    # Write dev data
    with open("data/dev.jsonl", "w", encoding="utf-8") as f:
        for item in dev_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"Generated {len(dev_data)} dev examples")
    print("Data generation complete!")


if __name__ == "__main__":
    main()
