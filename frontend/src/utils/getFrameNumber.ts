export const getFrameNumber = (frame: string): string => {
  const frameSplit = frame.split("/");
  const lastPart = frameSplit.at(-1);
  if (!lastPart) return "";
  const frameNumber = lastPart.split("_").at(-1)?.split(".")[0] ?? "";
  return frameNumber;
};
