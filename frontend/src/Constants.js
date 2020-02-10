// Constants.js

const prod = {
  api_url: "http://0.0.0.0:8080"
};

const dev = {
  api_url: "http://localhost:8000"
};
export const config = process.env.NODE_ENV === "development" ? dev : prod;
