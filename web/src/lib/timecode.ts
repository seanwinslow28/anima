/**
 * REEL ONE burn-in timecode. A board frame at `frameIndex` with a per-frame
 * `hold` has elapsed frameIndex × hold film frames at `fps` (12 by default —
 * the pipeline's frame rate). Rendered "HH:MM:SS+FF" with FF the residual
 * frames field, every field zero-padded to two digits.
 */
export function TC(frameIndex: number, hold: number, fps = 12): string {
  const filmFrames = frameIndex * hold;
  const totalSeconds = Math.floor(filmFrames / fps);
  const ff = filmFrames % fps;
  const hh = Math.floor(totalSeconds / 3600);
  const mm = Math.floor((totalSeconds % 3600) / 60);
  const ss = totalSeconds % 60;
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(hh)}:${pad(mm)}:${pad(ss)}+${pad(ff)}`;
}
