import './App.css';
import CommentStream from './components/CommentStream';
import Header from './components/Header';
import YoutubeStream from './components/YoutubeStream';

function App() {
  return (
    <div className="App" style={{backgroundColor:"ThreeDHighlight"}}>
      <div>
        <Header />
      </div>
      <div className="grid grid-cols-3 gap-4 h-screen items-center justify-center">
        <div className="col-span-2">
          <YoutubeStream />
        </div>
        <div>
          <CommentStream />
        </div>
      </div>
    </div>
  );
}

export default App;
