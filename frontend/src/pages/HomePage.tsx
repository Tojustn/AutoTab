import React, { useState } from "react";
import api from "../api.ts";
import { Button, CircularProgress, TextField, Box } from "@mui/material";
import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import NavBar from "../components/NavBar.tsx";

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

const HomePage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const formData = new FormData(event.currentTarget);
      const files = formData.getAll("files") as File[];
      if (files.length !== 1) {
        alert("Only one file is allowed");
        return;
      }
      if (
        formData.get("secondsPerFrame") &&
        (formData.get("secondsPerFrame") <= 0 ||
          formData.get("secondsPerFrame").toString().split(".")[1]?.length > 2)
      ) {
        alert("Seconds per frame must be greater than 0");
        return;
      }
      api
        .post("/upload", formData)
        .then((response: any) => console.log(response))
        .catch((error: any) => console.error(error));
    } catch (error) {
      console.error(error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log(event.target.files);
  };

  return (
    <Box
      className="min-h-screen w-screen items-center "
      sx={{ bgcolor: "background.default", color: "text.primary" }}
    >
      <NavBar />
      <div className="flex flex-col items-center justify-center h-dvh w-full">
        {isLoading ? (
          <CircularProgress className="text-center py-1 px-1" />
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-row items-center">
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
                  name="files"
                  onChange={handleFileChange}
                  multiple
                />
              </Button>
            </Box>
            <Box>
              <TextField
                name="secondsPerFrame"
                id="filled-number"
                label="Seconds per Frame Extracted(optional)"
                type="number"
                variant="filled"
                margin="dense"
                slotProps={{
                  inputLabel: {
                    shrink: true,
                  },
                }}
              />
            </Box>
            <Box m={2} p={2}>
              <Button type="submit" variant="contained">
                Submit
              </Button>
            </Box>
          </form>
        )}
      </div>
    </Box>
  );
};

export default HomePage;
