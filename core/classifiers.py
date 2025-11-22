import numpy as np

class MountBasedClassifier:
    @staticmethod
    def classify_heart_line_length(line_start, line_end, mounts):
        '''Classify heart line length based on mounts'''
        jupiter_x = mounts['mount_jupiter'][0]
        jupiter_y = mounts['mount_jupiter'][1]
        saturn_x = mounts['mount_saturn'][0]
        saturn_y = mounts['mount_saturn'][1]
        apollo_x = mounts['mount_apollo'][0]
        
        line_end_x = line_end[0]
        line_end_y = line_end[1]
        
        jupiter_saturn_distance = abs(jupiter_x - saturn_x)
        dist_to_jupiter = abs(line_end_x - jupiter_x)
        dist_to_saturn = abs(line_end_x - saturn_x)
        
        # LONG: At Jupiter OR between Jupiter and Saturn
        if dist_to_jupiter <= jupiter_saturn_distance * 0.4:
            return 'long'
        
        if jupiter_x < saturn_x:
            if jupiter_x <= line_end_x <= saturn_x:
                return 'long'
        else:
            if saturn_x <= line_end_x <= jupiter_x:
                return 'long'
        
        # MEDIUM: Near Saturn
        if dist_to_saturn <= jupiter_saturn_distance * 0.5:
            return 'medium'
        
        # SHORT: Beyond Saturn toward Apollo/Mercury
        dist_to_apollo = abs(line_end_x - apollo_x)
        if dist_to_apollo < dist_to_saturn:
            return 'short'
        
        return 'short'

    @staticmethod
    def classify_line_length_by_mounts(line_start, line_end, line_type, mounts):
        '''Classify line length based on palmistry rules'''
        if line_type == 'heart':
            return MountBasedClassifier.classify_heart_line_length(line_start, line_end, mounts)
        
        elif line_type == 'life':
            line_end_y = line_end[1]
            wrist_y = mounts['wrist'][1]
            saturn_y = mounts['mount_saturn'][1]
            palm_height = abs(wrist_y - saturn_y)
            
            lower_zone_threshold = saturn_y + (palm_height * 0.6)
            mid_zone_threshold = saturn_y + (palm_height * 0.35)
            
            if line_end_y >= lower_zone_threshold:
                return 'long'
            elif line_end_y >= mid_zone_threshold:
                return 'medium'
            else:
                return 'short'
        
        elif line_type == 'head':
            line_start_x = line_start[0]
            line_end_x = line_end[0]
            venus_x = mounts['mount_venus'][0]
            moon_x = mounts['mount_moon'][0]
            palm_center_x = (venus_x + moon_x) / 2
            palm_width = abs(moon_x - venus_x)
            
            if line_start_x < palm_center_x:
                if abs(line_end_x - moon_x) < palm_width * 0.3:
                    return 'long'
                elif line_end_x > palm_center_x:
                    return 'medium'
                else:
                    return 'short'
            else:
                if abs(line_end_x - venus_x) < palm_width * 0.3:
                    return 'long'
                elif line_end_x < palm_center_x:
                    return 'medium'
                else:
                    return 'short'
        
        elif line_type == 'fate':
            line_end_y = line_end[1]
            saturn_y = mounts['mount_saturn'][1]
            wrist_y = mounts['wrist'][1]
            palm_height = abs(wrist_y - saturn_y)
            
            upper_zone_threshold = saturn_y + (palm_height * 0.25)
            mid_zone_threshold = saturn_y + (palm_height * 0.5)
            
            if line_end_y <= upper_zone_threshold:
                return 'long'
            elif line_end_y <= mid_zone_threshold:
                return 'medium'
            else:
                return 'short'
        
        return 'medium'