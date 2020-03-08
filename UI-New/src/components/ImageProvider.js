import React from 'react';

const ImageProvider = (props) => (
  <div className={props.className}>
    <img src={props.src}/>
  </div>
);

export default ImageProvider;
