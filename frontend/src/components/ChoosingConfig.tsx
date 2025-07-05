import { useState, useEffect } from "react";
import { Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { getFrameNumber } from "../utils/getFrameNumber.ts";
import ReactCrop, { type Crop } from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";
import api from "../api";

interface ChoosingConfigProps {
  setCurrentPhase: (phase: string) => void;
  setIsLoading: (loading: boolean) => void;
  setLoadingMessage: (message: string) => void;
  setResult: (result: string) => void;
}

const ChoosingConfig = (props: ChoosingConfigProps) => {
  const [crop, setCrop] = useState<Crop>({
    unit: "px",
    x: 25,
    y: 25,
    width: 50,
    height: 50,
  });
  const { setCurrentPhase, setIsLoading, setLoadingMessage, setResult } = props;
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const fetchFrame = async () => {
      try {
        const response = await api.get("/get_frame", {
          withCredentials: true,
        });
        setFrame(response.data);
      } catch (error) {
        alert("Failed to fetch frame.");
        await api.post("/cleanup", {}, { withCredentials: true });
        setCurrentPhase("uploading");
      }
    };

    fetchFrame();
  }, []);

  const submitCrop = async () => {
    try {
      setIsLoading(true);
      setLoadingMessage("Predicting and Formatting Tabs");
      const form = new FormData();
      form.append(
        "dimensions",
        JSON.stringify({
          x: crop.x,
          y: crop.y,
          width: crop.width,
          height: crop.height,
        })
      );
      const response = await api.post("/confirmed_frames", form, {
        withCredentials: true,
      });
      setResult(response.data);
      setCurrentPhase("results");
      setIsLoading(false);
    } catch (error) {
      alert(error);
      await api.post("/cleanup", {}, { withCredentials: true });
      setCurrentPhase("upload");
      setIsLoading(false);
    }
  };
  return (
    <div className="flex justify-center items-center">
      {frame ? (
        <form onSubmit={submitCrop} className="flex flex-col">
          <p className="my-3">
            x: {crop.x.toFixed(2)} y: {crop.y.toFixed(2)} w:{" "}
            {crop.width.toFixed(2)} h: {crop.height.toFixed(2)}
          </p>
          <ReactCrop crop={crop} onChange={setCrop}>
            <img
              src={`http://127.0.0.1:5000${frame}`}
              key={getFrameNumber(frame)}
              alt="Extracted Frame"
            />
          </ReactCrop>
          <Button
            className="my-10 rounded-2xl"
            variant="contained"
            type="submit"
            endIcon={<SendIcon />}
          >
            Submit
          </Button>
        </form>
      ) : (
        <p>No frame available</p>
      )}
    </div>
  );
};

export default ChoosingConfig;
