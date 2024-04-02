import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
} from "react-admin";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { CustomersList } from "./Customers";
import { CustomerCreate } from "./CustomerCreate";

export const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource
      name="customer"
      list={CustomersList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={CustomerCreate}
    />
  </Admin>
);
