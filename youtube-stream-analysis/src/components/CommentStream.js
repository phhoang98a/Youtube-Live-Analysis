import React, { useState, useEffect, useRef } from 'react';
import Comments from './Comments';

const CommentStream = () => {
  const [data, setData] = useState([]);

  const commentContainerRef = useRef(null);

  useEffect(() => {
    const eventSource = new EventSource('http://127.0.0.1:3000/stream');
    eventSource.onmessage = function (event) {
      const newData = JSON.parse(event.data);
      setData((prevData) => [...prevData, newData]);
      console.log("Received data:", newData);
    };
    eventSource.onerror = (error) => {
      console.error('EventSource error:', error);
    };
    return () => {
      eventSource.close();
    };
  }, []);

  useEffect(() => {
    // Scroll to the bottom when messages change
    if (commentContainerRef.current) {
      commentContainerRef.current.scrollTop = commentContainerRef.current.scrollHeight;
    }
  }, [data]);

  return (
    <div className='flex flex-col lg:flex-row w-full h-screen overflow-y-auto justify-around px-2 py-20'>
      <div className='px-4 flex flex-col w-full bg-transparent overflow-hidden border border-1 border-gray-400/50 rounded-md py-2 shadow-md '>
        <div className='flex justify-between p-2 shadow-md'>
          <span className='text-white'>Top Chat</span>
        </div>
        <div className='w-full overflow-y-auto h-full overflow-hidden'>
          <div ref={commentContainerRef} className='h-full overflow-y-auto py-10'>
            {data.map((comment, index) => (
              <Comments key={index} data={comment} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommentStream;
