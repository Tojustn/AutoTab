from flask import current_app as app
from app.api.GuitarTabs import Tab
from collections import defaultdict

FRET_MAPPING = {
    "fret_1": "1",
    "fret_2": "2", 
    "fret_3": "3",
    "fret_4": "4",
    "fret_5": "5",
    "fret_6": "6",
    "fret_7": "7",
    "fret_8": "8",
    "fret_9": "9",
    "X": "X"
}

def render_tabs():
    note_list = ["e", "B", "G", "D", "A", "E"]
    note_list_copy = note_list.copy()
    start_of_line =  "e-\nB-\nG-\nD-\nA-\nE-"
    height, width = app.tracker.get_height(), app.tracker.get_width()
    strings = app.tracker.get_strings()
    string_locations_y = set()
    for string in strings:
        string_locations_y.add(string[1])
    # Sort string locations in descending order
    string_locations_y = sorted(string_locations_y, reverse=True)

    class_strings = {}
    for string in string_locations_y:
        class_strings[string] = note_list_copy.pop()
    if len(class_strings) != 6:
        return {"success": False, "status": 400, "message": "Could not classify strings"}
    # We have the locations of each of the notes in the string
        
    
    frets_per_frame = {}
    tabs = app.tracker.get_tabs()
    for tab in tabs:
        frame = tab.get_frame()
        frets_per_frame[frame] = frets_per_frame.get(frame, 0) + 1
    # Get the maximum number of frets in a frame
    max_frets_in_frame = max(frets_per_frame.values())

    print(f"Frets per frame: {frets_per_frame}")
    # Sort by frames then by position in x
    sorted_tabs = sorted(tabs, key = lambda x: (x.get_frame(), x.get_position()[0]))


    # Make a dictionary which stores the tabs in each frame
    tabs_per_frame = defaultdict(list)
    for tab in sorted_tabs:
        tabs_per_frame[tab.get_frame()].append(tab)
    
    # Sort each frame by position in x in ascending order and secondarily by position in y in descending order
    for frame in tabs_per_frame:
        tabs_per_frame[frame].sort(key = lambda x: (x.get_position()[0], -x.get_position()[1]))

    # Store all tab frames for final combination
    all_tab_frames = []
   
   
    for frame in sorted(tabs_per_frame):
        # Use a pointer for x and one for y
        current_x = 0
        current_y = 5  # Initialize current_y at the beginning of each frame
        tab_frames = [ [] for i in range(6)]
        previous_tab_bounding_box = None
        
        print(f"Starting frame {frame} with current_y = {current_y}")
        
        for tab in tabs_per_frame[frame]:
            # Make Bounding Boxes for each tab
            # get_position() returns (x1, y1, x2, y2) coordinates
            x1, y1, x2, y2 = tab.get_position()
            min_x = x1
            max_x = x2
            min_y = y1
            max_y = y2
            
                        # String of the frame -1 is at e and 6 is at E
            tab_string = None
            for i, string in enumerate(string_locations_y):
                if string >= min_y and string <= max_y:
                    tab_string = i
            fret_number = FRET_MAPPING.get(tab.get_fret(),0)
            # Check if we've moved to a new x position 
            if previous_tab_bounding_box is not None:
                prev_min_x, prev_max_x, prev_min_y, prev_max_y = previous_tab_bounding_box
                
                # Check if current tab's bounding box intersects with previous tab's bounding box
                # If they don't intersect horizontally, we've moved to a new time position
                x_intersects = not (min_x > prev_max_x or max_x < prev_min_x)
                
                print(f"X intersects: {x_intersects}")
                if not x_intersects:
                    while current_y > -1:
                        print(f"Current y: {current_y} Tab string: {tab_string}")
                        if current_y == tab_string:
                            tab_frames[current_y].append(f"-{fret_number}-")
                        else:
                            tab_frames[current_y].append(f"---")
                            #print(f"Tab string: {tab_string} current_y: {current_y} Frame: {frame}")
                        current_y -= 1

                    # Reset for new time position
                    current_y = 5
                    current_x += 1
                    previous_tab_bounding_box = None
                    continue


            print(f"Tab string: {tab_string} Fret: {tab.get_fret()} current_y: {current_y} Frame: {frame}")
            if tab_string is None:
                return {"success": False, "status": 400, "message": "Could not classify string"}
            
            print(f"Before check - current_y: {current_y}, tab_string: {tab_string}")
            if current_y != tab_string and current_y >= 0:
                tab_frames[current_y].append("---")
                current_y -= 1
            elif current_y == tab_string:
                tab_frames[current_y].append(f"-{fret_number}-")
            if current_y < 0:
                current_y = 5 
                current_x += 1
            previous_tab_bounding_box = (min_x, max_x, min_y, max_y)

        all_tab_frames.append(tab_frames)

    final_result = "" 
    print(all_tab_frames)
    for frame in all_tab_frames:
        for i in range(len(frame)-1,-1,-1):
            string_name = note_list[i]
            line = ''.join(frame[i])
            final_result += f"{string_name}|-{line}\n"

        final_result += "\n"

    print(final_result)

    
    return {
        "success": True, 
        "status": 200, 
        "result": final_result,
        "frames_processed": len(all_tab_frames)
    }