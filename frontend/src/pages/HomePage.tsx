import React, { useState } from "react";
import api from "../api.ts";
import { CircularProgress, Box } from "@mui/material";
import NavBar from "../components/NavBar.tsx";
import UploadConfig from "../components/UploadConfig.tsx";
import ChoosingConfig from "../components/ChoosingConfig.tsx";
import ResultConfig from "../components/ResultConfig.tsx";
import HowToUse from "../components/HowToUse.tsx";

const HomePage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState("");
  // Current phase of the loading process
  const [currentPhase, setCurrentPhase] = useState<
    "upload" | "choosing" | "results"
  >("upload");
  const [loadingMessage, setLoadingMessage] = useState("");

  const phaseMap = {
    upload: (
      <UploadConfig
        setLoadingMessage={setLoadingMessage}
        setCurrentPhase={setCurrentPhase}
        setIsLoading={setIsLoading}
      />
    ),
    choosing: (
      <ChoosingConfig
        setLoadingMessage={setLoadingMessage}
        setCurrentPhase={setCurrentPhase}
        setIsLoading={setIsLoading}
        setResult={setResult}
      />
    ),
    results: <ResultConfig result={result} />,
  };

  return (
    <Box
      className="h-screen w-screen items-center overflow-hidden"
      sx={{ bgcolor: "background.default", color: "text.primary" }}
    >
      <NavBar />
      <div className="flex flex-col items-center justify-center h-screen w-full ">
        {isLoading ? (
          <div className="flex flex-col items-center">
            <CircularProgress className="text-center py-1 px-1" size={50} />
            <h2> {loadingMessage}</h2>
          </div>
        ) : (
          phaseMap[currentPhase]
        )}
        <HowToUse />
      </div>
    </Box>
  );
};

export default HomePage;
