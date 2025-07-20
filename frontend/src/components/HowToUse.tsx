import { Box } from "@mui/material";

const HowToUse = () => {
  return (
    <Box sx={{ color: "text.primary" }}>
      <label className="font-bold">How to use:</label>
      <ol className="list-decimal ">
        <li>Upload a guitar video- Make sure the first frame shows the tabs</li>
        <li>
          Select how frames are extracted: either set a time interval (e.g.,
          every 1 second) or specify exact timestamps for each frame you want to
          capture.
        </li>
        <li>Set crop dimensions- Highlight the area where tabs appear.</li>
        <li>
          View your tabs- The site will generate and display guitar tabs based
          on the selected frames.
        </li>
      </ol>
    </Box>
  );
};

export default HowToUse;
