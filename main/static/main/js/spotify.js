function authSpotify() {
    fetch("is-authenticated")
    .then((response) => response.json())
    .then((data) => {
    //   this.setState({ spotifyAuthenticated: data.status });
      console.log(data.status);
      if (!data.status) {
        fetch("get-auth-url")
          .then((response) => response.json())
          .then((data) => {
            window.location.replace(data.url);
          });
      }
    });
}