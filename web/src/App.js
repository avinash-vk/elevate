import { Route, Switch, BrowserRouter, Redirect } from "react-router-dom";
import ROUTES from "./routes";
import React from 'react';

import { AuthContext } from "./firebase/provider";

import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import SignIn from "./pages/auth/Signin";
import Landing from "./pages/Landing";
import SignUp from './pages/auth/Signup';
import { auth } from "./firebase";

function App() {
  let { user, setUser } = React.useContext(AuthContext);
  const [loading, setLoading] = React.useState(false);
  /*
  React.useEffect(() => {
      if(user){
        setUser(user)
      }
      else {
        setUser(null);
      }
      setLoading(false);
  },[])
  */
  if(loading) return <p>Loading...</p>
  let signedInRoutes = (
    <Switch>
      <Route exact path={ROUTES.dashboard} component={Dashboard} />
      <Route exact path={ROUTES.profile} component={Profile} />
      <Route exact path={ROUTES.settings} component={Settings} />
      <Redirect to={ROUTES.dashboard} />
    </Switch>
  );
  let signedOutRoutes = (
    <Switch>
      <Route exact path={ROUTES.signin} component={()=><SignIn setUser = {setUser} />} />
      <Route exact path={ROUTES.signup} component={SignUp} />
      <Route exact path={ROUTES.landing} component = {Landing} />
      <Redirect to={ROUTES.landing} />
    </Switch>
  );
  return (
    <BrowserRouter>
      {
        user 
        ? <> {signedInRoutes} </>
        : <> {signedOutRoutes} </>
      }
    </BrowserRouter>
  );
}
export default App;
