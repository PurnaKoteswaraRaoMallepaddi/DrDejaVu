interface AudioPlayerProps {
  src: string;
}

export default function AudioPlayer({ src }: AudioPlayerProps) {
  const handleError = (e: React.SyntheticEvent<HTMLAudioElement>) => {
    const audio = e.currentTarget;
    console.error("[AudioPlayer] Failed to load audio:", {
      src,
      error: audio.error?.message,
      readyState: audio.readyState,
      networkState: audio.networkState,
    });
  };

  return (
    <div className="audio-player">
      <audio 
        controls 
        src={src}
        onError={handleError}
        preload="metadata"
      >
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}
