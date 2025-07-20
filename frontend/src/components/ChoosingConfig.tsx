import { useState, useEffect } from "react";
import { Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { getFrameNumber } from "../utils/getFrameNumber.ts";
import ReactCrop, { type Crop } from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";
import api from "../api";

type ChoosingConfigProps = {
  setCurrentPhase: React.Dispatch<
    React.SetStateAction<"upload" | "choosing" | "results">
  >;
  setIsLoading: (loading: boolean) => void;
  setLoadingMessage: (message: string) => void;
  setResult: (result: string) => void;
};

const ChoosingConfig = (props: ChoosingConfigProps) => {
  const [crop, setCrop] = useState<Crop>({
    unit: "px",
    x: 10,
    y: 10,
    width: 50,
    height: 50,
  });
  const { setCurrentPhase, setIsLoading, setLoadingMessage, setResult } = props;
  const [frame, setFrame] = useState<string | null>(null);
  const [imgRef, setImgRef] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    const fetchFrame = async () => {
      try {
        const response = await api.get("/get_frame", {
          withCredentials: true,
        });
        if (response.data.success === false) {
          throw new Error(response.data.message);
        }
        setFrame(response.data);
      } catch (error) {
        alert(error);
        await api.post("/cleanup", {}, { withCredentials: true });
        setCurrentPhase("upload");
        setIsLoading(false);
      }
    };

    fetchFrame();
  }, []);

  const submitCrop = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!imgRef) return;
    // Calculate scale factors
    const naturalWidth = imgRef.naturalWidth;
    const naturalHeight = imgRef.naturalHeight;
    const displayedWidth = imgRef.width;
    const displayedHeight = imgRef.height;
    const scaleX = naturalWidth / displayedWidth;
    const scaleY = naturalHeight / displayedHeight;
    // Convert crop values
    const cropX = crop.x * scaleX;
    const cropY = crop.y * scaleY;
    const cropWidth = crop.width * scaleX;
    const cropHeight = crop.height * scaleY;
    console.log("Submitting crop with dimensions:", {
      x: cropX,
      y: cropY,
      width: cropWidth,
      height: cropHeight,
    });
    try {
      setIsLoading(true);
      setLoadingMessage("Predicting and Formatting Tabs");
      const form = new FormData();
      alert(
        `Final Dimensions:\n` +
          `x: ${Math.round(cropX)}\n` +
          `y: ${Math.round(cropY)}\n` +
          `width: ${Math.round(cropWidth)}\n` +
          `height: ${Math.round(cropHeight)}`
      );
      form.append(
        "dimensions",
        JSON.stringify({
          x: cropX,
          y: cropY,
          width: cropWidth,
          height: cropHeight,
        })
      );
      const response = await api.post("/confirmed_frames", form, {
        withCredentials: true,
      });
      setResult(response.data.result);
      setCurrentPhase("results");
      setIsLoading(false);
    } catch (error) {
      alert(error);
      try {
        await api.delete("/cleanup", { withCredentials: true });
      } finally {
        setCurrentPhase("upload");
        setIsLoading(false);
      }
    }
  };
  const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || "5000";
  return (
    <div className="flex justify-center items-center">
      {frame ? (
        <form onSubmit={submitCrop} className="flex flex-col">
          <p className="my-3">
            x: {crop.x.toFixed(2)}px y: {crop.y.toFixed(2)}px w:{" "}
            {crop.width.toFixed(2)}px h: {crop.height.toFixed(2)}px
          </p>
          <ReactCrop crop={crop} onChange={(c) => setCrop(c)}>
            <img
              src={`http://localhost:${BACKEND_PORT}${frame}`}
              key={getFrameNumber(frame)}
              alt="Extracted Frame"
              style={{ maxWidth: 1000, maxHeight: 1000 }}
              ref={setImgRef}
              onLoad={(e) => setImgRef(e.currentTarget)}
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
