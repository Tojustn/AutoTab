import React from "react";
import { Box } from "@mui/material";

const ResultConfig = ({ result }: { result: string }) => {
  return (
    <Box className="flex flex-col">
      <h1>Result</h1>
      <label>AutoTab Formatter</label>
      <textarea
        value={result}
        style={{ width: 1000, fontFamily: "monospace" }}
      ></textarea>
    </Box>
  );
};

export default ResultConfig;
