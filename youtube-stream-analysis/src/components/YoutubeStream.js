import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const VideoStream = () => {
  const [imageSrc, setImageSrc] = useState(null);
  
  useEffect(() => {
    // Connect to Socket.IO server
    const socket = io('http://localhost:5050');

    // Listen for incoming frames
    socket.on('video_frame', (frameData) => {
      setImageSrc(`data:image/jpeg;base64,${frameData}`);
    });

    // Cleanup on component unmount
    return () => socket.disconnect();
  }, []);

  return (
    <div className='flex items-center justify-center'>
      {imageSrc && (
        <img src={imageSrc} className="rounded-lg" style={{ width: '1000px' }} alt="Streamed content" />
      )}
    </div>
  );
};

export default VideoStream;
