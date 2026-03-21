interface AudioPlayerProps {
  src: string;
}

export default function AudioPlayer({ src }: AudioPlayerProps) {
  return (
    <div className="audio-player">
      <audio controls src={src}>
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}
