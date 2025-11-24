class VedicInterpreter:
    @staticmethod
    def interpret_life_line_detailed_vedic(features):
        '''Highly detailed Vedic life line interpretation (Jeevan Rekha)'''
        interpretation = []
        
        # Length interpretation
        length = features.get('length', 'medium')
        if length == 'long':
            interpretation.append("Long Jeevan Rekha indicates exceptional vitality, strong pranic energy flow, and excellent capacity for recovery from setbacks - blessed with robust health and endurance throughout life's journey.")
        elif length == 'short':
            interpretation.append("Short Jeevan Rekha suggests need for energy conservation and mindful pacing - does not indicate short lifespan but rather cautious energy expenditure, with success through strategic rest and rejuvenation practices.")
        else:
            interpretation.append("Medium Jeevan Rekha shows balanced vitality with steady energy reserves for life's demands.")
        
        # Depth and clarity
        depth = features.get('depth', 'medium')
        clarity = features.get('clarity', 'clear')
        if depth == 'deep' and clarity == 'clear':
            interpretation.append("Deep and clear line reveals strong physical constitution, focused life path with minimal deviations, and powerful determination - karma of good health from past lives manifesting.")
        elif depth == 'shallow' or clarity == 'faint':
            interpretation.append("Faint or shallow marking indicates sensitive nervous system, fluctuating energy levels, or vata dosha imbalance requiring grounding practices, pranayama, and ashwagandha supplementation.")
        
        # Curvature
        curve = features.get('curve', 'normal')
        if curve == 'wide':
            interpretation.append("Wide sweeping curve toward palm center indicates adventurous spirit, extroverted nature, high physical activity levels, and strong connection to material world - ideal for dynamic careers and social leadership.")
        elif curve == 'narrow':
            interpretation.append("Tight curve close to thumb mount suggests introverted temperament, cautious approach, preference for mental over physical activities, and need for personal sanctuary.")
        
        # Chains and breaks
        if features.get('chained', False):
            interpretation.append("Chained pattern (small interconnected loops) indicates karmic challenges manifesting as health fluctuations, confusion in life direction, emotional turbulence - periods of prarabdha karma requiring acceptance and spiritual practices for stability.")
        
        if features.get('breaks', 0) > 0:
            interpretation.append("Breaks in line signify major life transformations, significant health events, or complete directional shifts - if overlapping or protected by sister line, indicates successful recovery and emergence stronger after crisis.")
        
        # Islands
        if features.get('islands', 0) > 0:
            interpretation.append("Islands reveal temporary weakness periods, health vulnerabilities, or energy depletion phases requiring medical attention, rest, and karmic remediation through charity and mantra.")
        
        # Forks and branches
        if features.get('fork_end', False):
            interpretation.append("Fork at termination (trident if three-pronged) is highly auspicious - indicates desire for travel in later life, multiple paths of success, or geographic relocation bringing prosperity.")
        
        if features.get('upward_branches', 0) > 0:
            interpretation.append("Upward branches emanating toward fingers show resilience, ability to overcome obstacles, periods of success and recognition - each branch marks achievement milestone or spiritual elevation.")
        
        if features.get('downward_branches', 0) > 0:
            interpretation.append("Downward branches indicate challenges to vitality, possible health setbacks, or phases requiring caution - strength of mind and ayurvedic lifestyle modifications can mitigate effects.")
        
        # Sister/parallel line
        if features.get('sister_line', False):
            interpretation.append("Parallel sister line (Jeevan Rekha guardian) provides divine protection, indicates support from family or spiritual guides, doubles vitality, and ensures recovery from any life-threatening situations.")
        
        # Dosha indicators
        if features.get('color', 'pink') == 'red':
            interpretation.append("Reddish hue indicates pitta dominance - strong digestive fire, leadership qualities, but tendency toward inflammation and anger requiring cooling practices.")
        elif features.get('color', 'pink') == 'pale':
            interpretation.append("Pale coloration suggests kapha imbalance or anemia - need for iron-rich diet, blood-building herbs, and energizing practices.")
        
        return " ".join(interpretation) if interpretation else "Life line shows balanced characteristics requiring deeper analysis with astrological birth chart correlation."
    
    @staticmethod
    def interpret_heart_line_detailed_vedic(features):
        '''Highly detailed Vedic heart line interpretation (Hridaya Rekha)'''
        interpretation = []
        
        # Starting and ending points
        start = features.get('start_position', 'below_mercury')
        end = features.get('end_position', 'between_jupiter_saturn')
        
        if end == 'jupiter':
            interpretation.append("Hridaya Rekha ending at Jupiter mount indicates idealistic romantic nature, capacity for unconditional love, spiritual approach to relationships, and tendency to place partners on pedestals - blessed with devotional heart chakra.")
        elif end == 'saturn':
            interpretation.append("Line terminating below Saturn finger reveals emotional restraint, difficulty expressing vulnerability, duty-oriented approach to relationships, and tendency to prioritize career over intimacy - need for heart-opening practices.")
        elif end == 'between_jupiter_saturn':
            interpretation.append("Ending between Jupiter and Saturn shows balanced emotional expression - neither overly idealistic nor excessively reserved, practical yet affectionate in love matters.")
        
        # Shape and curve
        shape = features.get('shape', 'curved')
        if shape == 'curved':
            interpretation.append("Curved Hridaya Rekha signifies warm, open-hearted nature with strong need for affection, expressive emotional style, nurturing qualities, and ability to form deep bonds - natural counselor and healer.")
        elif shape == 'straight':
            interpretation.append("Straight line indicates pragmatic, logical approach to emotions, straightforward relationship style, selective expression of feelings, and mental processing of emotions before expressing.")
        
        length = features.get('length', 'medium')
        if length == 'long':
            interpretation.append("Long heart line extending across palm reveals intense emotional capacity, passionate nature, tendency toward jealousy or possessiveness, and all-consuming approach to love requiring conscious balance.")
        elif length == 'short':
            interpretation.append("Short Hridaya Rekha suggests self-contained emotional world, independence in relationships, difficulty with vulnerability, or past-life karma of emotional protection.")
        
        # Depth and clarity
        depth = features.get('depth', 'medium')
        if depth == 'deep':
            interpretation.append("Deep engraving indicates strong emotions, loyalty, capacity for profound love, and intense feelings that can lead to both great joy and deep suffering - powerful heart chakra requiring spiritual maturity.")
        elif depth == 'shallow':
            interpretation.append("Faint line suggests superficial emotional connections, difficulty sustaining relationships, fear of intimacy, or emotional immaturity requiring heart-centered meditation and relationship healing work.")
        
        # Breaks and chains
        if features.get('breaks', 0) > 0:
            interpretation.append("Breaks signify emotional upheavals, significant heartbreaks, betrayals, or divorce - each break represents karmic lesson in love, with healing occurring through time and spiritual growth practices.")
        
        if features.get('chained', False):
            interpretation.append("Chained pattern reveals phases of emotional turbulence, relationship stress, confusion in love matters, or oscillating between partners - indicates unresolved heart chakra blockages requiring energy healing.")
        
        # Islands
        if features.get('islands', 0) > 0:
            interpretation.append("Islands on Hridaya Rekha indicate periods of depression, emotional crisis, relationship complications, or heart-related health concerns - location on line reveals timing through palmistry chronology.")
        
        # Forks and branches
        if features.get('fork_end', False):
            interpretation.append("Forked ending shows ability to see multiple perspectives in relationships, diplomatic emotional nature, or split between heart and mind in decision-making - indicates emotional complexity and adaptability.")
        
        if features.get('multiple_branches', False):
            interpretation.append("Multiple branches pointing upward signify complex love life with several significant emotional connections, polyamorous tendencies, or multiple marriages - each branch represents important relationship influence.")
        
        # Connection with head line
        if features.get('merged_with_head_line', False):
            interpretation.append("Merger with head line (Mastak Rekha) creates 'Simian line' indicating intense personality, difficulty separating emotions from logic, powerful willpower, and karmic indication of singular life purpose.")
        
        # Special markings
        if features.get('star', False):
            interpretation.append("Star marking is highly auspicious - indicates extraordinary love, soulmate connection, or significant romantic blessing arriving at specific life period.")
        
        if features.get('cross', False):
            interpretation.append("Cross symbol warns of emotional challenges, relationship obstacles, or heartbreak requiring karmic remediation through Venus mantras and gemstone therapy (diamond or white sapphire).")
        
        return " ".join(interpretation) if interpretation else "Heart line indicates emotional awareness developing - observe emotional patterns and practice heart-centered meditation for clarity."
    
    @staticmethod
    def interpret_head_line_detailed_vedic(features):
        '''Highly detailed Vedic head line interpretation (Mastak Rekha)'''
        interpretation = []
        
        # Length interpretation
        length = features.get('length', 'medium')
        if length == 'long':
            interpretation.append("Long Mastak Rekha extending below little finger reveals deep, thorough thinking capacity, tendency toward overanalysis, strong memory retention, and ability to see long-term consequences - blessed with Mercury's intellectual gifts.")
        elif length == 'short':
            interpretation.append("Short head line indicates quick, spontaneous thinking, practical intelligence over theoretical knowledge, ability to make rapid decisions without overthinking, and present-focused mentality.")
        else:
            interpretation.append("Medium-length line shows balanced mental approach combining analysis with action.")
        
        # Direction and curve
        direction = features.get('direction', 'straight')
        if direction == 'straight':
            interpretation.append("Straight horizontal Mastak Rekha signifies practical, logical mind, detail-oriented thinking, realistic worldview, preference for facts over imagination - ideal for analytical careers, engineering, mathematics, and scientific pursuits.")
        elif direction == 'curved_down':
            interpretation.append("Downward curving line toward Moon mount reveals creative, intuitive mind, artistic inclinations, strong imagination, tendency toward fantasy, and preference for subjective over objective thinking - gifted in arts, writing, music.")
        elif direction == 'steeply_sloped':
            interpretation.append("Steep slope into Moon mount indicates highly imaginative but potentially impractical mind, tendency toward escapism, depression risk, or difficulty grounding thoughts into material reality requiring root chakra work.")
        
        # Depth and clarity
        depth = features.get('depth', 'medium')
        clarity = features.get('clarity', 'clear')
        if depth == 'deep' and clarity == 'clear':
            interpretation.append("Deep, sharp line indicates mental clarity, focused concentration, strong reasoning capacity, excellent decision-making abilities, and stable thought patterns - Mercury and Jupiter blessings manifesting.")
        elif depth == 'shallow' or clarity == 'faint':
            interpretation.append("Faint or scattered line suggests fluctuating attention, difficulty concentrating, mental restlessness, vata imbalance affecting mind, or need for meditation, brahmi supplementation, and grounding practices.")
        
        # Starting point
        start = features.get('start_position', 'standard')
        if start == 'joined_with_life_line':
            interpretation.append("Origin merged with life line indicates cautious, careful nature, family influence on thinking, tendency to overthink before acting, and close connection between physical and mental energies.")
        elif start == 'separated_from_life_line':
            interpretation.append("Clear separation from life line reveals independent thinking, confidence, spontaneous decision-making, courage, and freedom from family mental conditioning - sign of self-made individual.")
        elif start == 'mars_mount':
            interpretation.append("Starting from Mars mount indicates aggressive thinking, argumentative nature, warrior mentality, ability to fight for beliefs, and tendency toward mental conflict requiring anger management practices.")
        
        # Breaks and chains
        if features.get('breaks', 0) > 0:
            interpretation.append("Breaks signify periods of significant mental change, thought pattern transformation, head injuries, nervous system disorders, or complete ideological shifts - each break represents mental death-rebirth cycle.")
        
        if features.get('chained', False):
            interpretation.append("Chained pattern indicates mental confusion, difficulty focusing, anxiety, tendency toward headaches or migraines, or karmic mental fog requiring clarity through Saraswati mantras and meditation.")
        
        # Islands
        if features.get('islands', 0) > 0:
            interpretation.append("Islands reveal periods of mental health challenges, memory problems, concentration difficulties, or specific learning disabilities - timing correlates with age using palmistry chronology system.")
        
        # Fork endings
        if features.get('fork_end', False):
            interpretation.append("Writer's fork (bifurcated ending) is highly auspicious - indicates dual thinking ability combining practical and creative, versatility, excellent writing skills, and ability to see multiple perspectives simultaneously.")
        
        if features.get('triple_fork', False):
            interpretation.append("Triple fork (trident ending) is extremely rare and fortunate - signifies genius-level intelligence, multidimensional thinking, balanced approach to all life aspects, and divine blessing of Saraswati goddess.")
        
        # Double head line
        if features.get('double_line', False):
            interpretation.append("Double Mastak Rekha reveals dual nature, ability to pursue two careers simultaneously, versatile thinking switching between analytical and creative modes, or indication of past-life intellectual achievements carried forward.")
        
        # Branches
        if features.get('upward_branches', 0) > 0:
            branch_location = features.get('branch_toward', 'general')
            if branch_location == 'jupiter':
                interpretation.append("Upward branch to Jupiter mount indicates ambition, leadership aspirations, desire for recognition, and periods where thinking focuses on expansion and growth.")
            elif branch_location == 'saturn':
                interpretation.append("Branch toward Saturn shows serious thinking phases, research orientation, interest in mysticism or occult sciences, and philosophical inclinations.")
            elif branch_location == 'sun':
                interpretation.append("Branch to Sun mount reveals creative thinking peaks, artistic achievements, recognition for intellectual work, and fame through mental abilities.")
            elif branch_location == 'mercury':
                interpretation.append("Branch toward Mercury signifies business acumen, communication skills, scientific thinking, or success in commerce and trade through intelligent strategies.")
            else:
                interpretation.append("Upward branches are highly favorable - indicate mental achievements, success through intellectual efforts, and positive thinking periods bringing opportunities.")
        
        if features.get('downward_branches', 0) > 0:
            interpretation.append("Downward branches especially in early portion are unfavorable - suggest mental setbacks, disappointing decisions, negative thinking phases, or periods of depression requiring spiritual intervention.")
        
        # Special markings
        if features.get('star', False):
            interpretation.append("Star marking indicates sudden mental brilliance, breakthrough insight, or possibility of head injury depending on location - powerful karmic indicator requiring careful analysis with other signs.")
        
        if features.get('square', False):
            interpretation.append("Square is protective symbol - indicates mental protection during crisis, ability to overcome psychological challenges, or divine intervention preventing mental breakdown.")
        
        if features.get('cross', False):
            interpretation.append("Cross suggests mental obstacles, accidents affecting head, or challenging thought patterns requiring karmic remediation through Jupiter-strengthening practices.")
        
        return " ".join(interpretation) if interpretation else "Head line shows developing mental faculties - practice meditation and pranayama for enhanced mental clarity and focus."
    
    @staticmethod
    def interpret_fate_line_detailed_vedic(features, present=True):
        '''Highly detailed Vedic fate line interpretation (Bhagya Rekha)'''
        if not present:
            return "Fate line absent (Bhagya Rekha not visible) - self-created destiny without predetermined path, complete free will in shaping life direction, success through personal initiative rather than external support or family influence, indication of kriyamana karma dominance over prarabdha karma, requiring self-discipline and strategic planning for achievement."
        
        interpretation = []
        
        # Starting point - crucial for timing
        start = features.get('start_position', 'base_palm')
        if start == 'base_palm':
            interpretation.append("Bhagya Rekha originating from wrist base indicates early life career focus, predetermined life path from childhood, strong family influence or inheritance, and destiny set in motion from birth - prarabdha karma strongly directing life course.")
        elif start == 'life_line':
            interpretation.append("Starting from life line (Jeevan Rekha) signifies self-made success through personal hard work rather than inheritance, struggle in early years transformed into achievement through effort, ideal for entrepreneurs and self-employed - complete responsibility for own destiny.")
        elif start == 'moon_mount':
            interpretation.append("Origin from Moon mount reveals destiny shaped by public, success depending on others' favor, career in public service or entertainment, and fortune through relationships - must cultivate people skills for achievement.")
        elif start == 'middle_palm':
            interpretation.append("Beginning from middle palm indicates late career clarity, significant life changes after age 35, delayed success requiring patience, or career transformation in middle age replacing earlier struggles.")
        
        # Ending point
        end = features.get('end_position', 'saturn')
        if end == 'saturn':
            interpretation.append("Terminating at Saturn mount (standard position) shows career culmination, professional peak in middle age, satisfaction through discipline and hard work, and traditional path to success through perseverance.")
        elif end == 'jupiter':
            interpretation.append("Ending at Jupiter mount indicates ambition fulfilled, leadership position attained, recognition and authority achieved, and destiny involving teaching, guiding, or ruling others - highly auspicious for power.")
        elif end == 'sun':
            interpretation.append("Terminating at Sun mount reveals success through creativity, fame and recognition, career in arts or public eye, and fortune through personal brilliance and charisma - Apollo's blessing manifesting.")
        elif end == 'mercury':
            interpretation.append("Ending at Mercury mount signifies success in business, communication, or science, wealth through intelligence and strategy, and achievement in commerce or technical fields - Mercury's mercantile blessings.")
        
        # Depth and clarity
        depth = features.get('depth', 'medium')
        clarity = features.get('clarity', 'clear')
        if depth == 'deep' and clarity == 'clear':
            interpretation.append("Deep, clear Bhagya Rekha indicates well-defined career path, steady professional progress, strong sense of life purpose, minimal career disruptions, and powerful prarabdha karma directing toward specific destiny.")
        elif depth == 'shallow' or clarity == 'faint':
            interpretation.append("Faint or broken line suggests career uncertainties, frequent job changes, difficulty finding life purpose, or dominance of kriyamana karma requiring conscious effort to create destiny.")
        
        # Breaks and gaps
        if features.get('breaks', 0) > 0:
            interpretation.append("Breaks signify career interruptions, job changes, business failures followed by new beginnings, or external circumstances forcing directional shifts - if line continues strongly after break, indicates successful recovery and adaptation.")
        
        # Forks
        if features.get('fork_start', False):
            interpretation.append("Fork at origin suggests multiple talents, dual career paths, or choice between two distinct life directions in early life - decision point shaping entire destiny trajectory.")
        
        if features.get('fork_end', False):
            interpretation.append("Forked ending indicates divergence into multiple interests in later career, diversification of income sources, or division of energy between competing professional paths requiring integration.")
        
        # Multiple fate lines
        if features.get('multiple_lines', False):
            interpretation.append("Multiple parallel Bhagya Rekhas reveal simultaneous careers, multiple income streams, diverse talents being expressed concurrently, or complex destiny requiring management of several life purposes.")
        
        # Lines joining fate line
        if features.get('lines_joining', 0) > 0:
            interpretation.append("Lines merging into fate line indicate external support, influential people entering life, partnerships benefiting career, or assistance arriving at crucial times - karma of receiving help manifesting.")
        
        # Islands
        if features.get('islands', 0) > 0:
            interpretation.append("Islands reveal career difficulties, professional scandals, reputation damage, or periods of professional confusion and setback - timing indicated by position on line using age calculation method.")
        
        # Squares
        if features.get('square', False):
            interpretation.append("Square marking provides divine protection during career crisis, indicates salvation from professional disaster, or shows ability to contain and overcome work-related problems through cosmic intervention.")
        
        # Stars
        if features.get('star', False):
            interpretation.append("Star on Bhagya Rekha is double-edged - can indicate sudden fame and success or sudden scandal and downfall depending on surrounding signs - represents karmic turning point requiring careful navigation.")
        
        # Crosses
        if features.get('cross', False):
            interpretation.append("Cross symbol warns of career obstacles, professional setbacks, enemies at work, or challenging periods requiring Saturn remedies including blue sapphire, black sesame charity, and Shani mantras.")
        
        # Relationship with other lines
        if features.get('crosses_life_line', False):
            interpretation.append("Intersection with life line indicates career affecting health or personal life dominating professional decisions at that age - integration point of personal and professional karma.")
        
        if features.get('parallel_to_life_line', False):
            interpretation.append("Running parallel to life line shows career and personal life in harmony, work aligned with vitality, or professional path supporting rather than draining life energy.")
        
        # Timing-based interpretation
        age = features.get('current_age_marker', None)
        if age:
            if age < 25:
                interpretation.append(f"At current life stage (age {age}), focus on education, skill development, and foundation building - early Bhagya Rekha phase requires preparation over immediate results.")
            elif 25 <= age < 40:
                interpretation.append(f"At age {age}, mid-career development phase - time for establishing professional identity, taking calculated risks, and building reputation through consistent effort.")
            elif 40 <= age < 55:
                interpretation.append(f"At age {age}, peak professional phase - harvest period for earlier efforts, leadership opportunities, maximum earning potential, and destiny manifestation.")
            else:
                interpretation.append(f"At age {age}, wisdom and mentorship phase - time for guiding others, legacy building, transitioning from doing to teaching, and preparing for spiritual focus.")
        
        # Karmic remedies suggestion
        if features.get('weak_fate_line', False):
            interpretation.append("Weak Bhagya Rekha requires karmic strengthening through Saturn worship - wear blue sapphire after astrological consultation, donate black sesame and iron on Saturdays, chant Shani mantras, and serve elderly or handicapped for destiny improvement.")
        
        return " ".join(interpretation) if interpretation else "Fate line shows karmic direction requiring observation over time - maintain career journal and consult Jyotish astrologer for precise timing of events based on Dasha system."
