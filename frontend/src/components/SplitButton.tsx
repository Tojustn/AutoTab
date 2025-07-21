import { Box, TextField, Switch } from "@mui/material";
import { useState } from "react";

type SplitButtonProps = {
  secondsPerFrame: number | undefined;
  setSecondsPerFrame: React.Dispatch<React.SetStateAction<number | undefined>>;
  selectedFrames: string;
  setSelectedFrames: React.Dispatch<React.SetStateAction<string>>;
};

export default function SplitButton({
  secondsPerFrame,
  setSecondsPerFrame,
  selectedFrames,
  setSelectedFrames,
}: SplitButtonProps) {
  const [intervalMode, setIntervalMode] = useState<boolean>(true);

  const handleToggle = () => {
    setIntervalMode((prev) => !prev);
    selectedFrames === ""
      ? setSecondsPerFrame(undefined)
      : setSelectedFrames("");
  };
  return (
    <Box>
      <Box>
        <Switch onChange={handleToggle} defaultChecked color="default" />
      </Box>
      <Box my={2}>
        <TextField
          id={intervalMode ? "interval-mode" : "select-mode"}
          label={intervalMode ? "Seconds per Frame " : "Timestamps "}
          type="text"
          helperText={
            intervalMode
              ? "Extract a frame every X seconds"
              : "Enter comma-separated times in seconds (e.g. 1,2,4,10)"
          }
          name={intervalMode ? "new_line" : "selected_frames"}
          value={intervalMode ? secondsPerFrame ?? "" : selectedFrames}
          onChange={(e) => {
            if (intervalMode) {
              setSecondsPerFrame(Number(e.target.value));
              console.log(selectedFrames);
            } else {
              setSelectedFrames(e.target.value);
              console.log(secondsPerFrame);
            }
          }}
        />
      </Box>
    </Box>
  );
}
