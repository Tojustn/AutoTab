import { Box, Button, TextField } from "@mui/material";
import SplitButton from "./SplitButton";
import { useState } from "react";
import api from "../api";

import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { styled } from "@mui/material/styles";

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});
const UploadConfig = (props: any) => {
  const { setLoadingMessage, setCurrentPhase, setIsLoading } = props;
  const [file, setFile] = useState<File | undefined>();
  const [secondsPerFrame, setSecondsPerFrame] = useState<number | undefined>();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSecondsPerFrameChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    console.log("changing seconds per frame");
    const value = event.target.value;
    setSecondsPerFrame(value === undefined ? undefined : Number(value));
  };

  const handleSubmitUpload = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    console.log("Submitting Upload");

    setIsLoading(true);
    setLoadingMessage("Uploading files...");
    event.preventDefault();
    const formData = new FormData();
    try {
      setCurrentPhase("upload");
      if (!file) {
        throw new Error("User must upload a file");
      }
      if (
        secondsPerFrame &&
        (Number(secondsPerFrame) <= 0 ||
          !Number.isFinite(Number(secondsPerFrame)))
      ) {
        throw new Error("Seconds per frame must be a positive integer");
      }

      formData.append("video", file);
      if (secondsPerFrame !== undefined) {
        formData.append("new_line", String(secondsPerFrame));
      }
      console.log(formData);
      const response = await api.post("/upload", formData, {
        withCredentials: true,
      });
      setIsLoading(false);
      if (response.data.success) {
        setCurrentPhase("choosing");
      } else {
        throw new Error(`${response.data.message}`);
      }
      console.log(response);
    } catch (error) {
      alert(error);
      setIsLoading(false);
      setFile(undefined);
      setSecondsPerFrame(undefined);
      setCurrentPhase("upload");
      console.log(error);
    }
  };

  return (
    <form onSubmit={handleSubmitUpload} className="flex flex-row items-center">
      <Box m={2}>
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<CloudUploadIcon />}
          className="px-4 py-2"
        >
          Upload files
          <VisuallyHiddenInput
            type="file"
            name="video"
            onChange={handleFileChange}
          />
        </Button>
      </Box>
      <SplitButton></SplitButton>
      <Box m={2} p={2}>
        <Button type="submit" variant="contained">
          Submit
        </Button>
      </Box>
    </form>
  );
};

export default UploadConfig;
