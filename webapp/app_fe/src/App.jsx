import './App.css'
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import HomePage from './components/HomePage/HomePage.jsx'
import ViewPage from './components/ViewPage/ViewPage.jsx'

function App() {

  return (  
    <BrowserRouter>
      <Routes>
        <Route path="/">
          <Route index element={<HomePage />} />
          <Route path="watch" element={<ViewPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
