import axios from "axios";
import { get } from "http";

interface PropsAPI {
  url: string;
}

const getAPI = async ({ url }: PropsAPI) => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/" + url);
    return response.data;
  } catch (error) {
    console.error("API request failed:", error);
    throw error;
  }
};

const fetchAPI = async (params: PropsAPI) => {
  try {
    const data = await getAPI(params);
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
};

export default fetchAPI;
