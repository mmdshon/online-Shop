import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
} from "react-admin";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { UsersList } from "./resource db/Users";
import { UsersCreate } from "./resource db/Userscreate";
import { OrdersList } from "./resource db/orders";
import { OrderCreat } from "./resource db/orderCreate";

export const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource
      name="Users"
      list={UsersList}
      edit={EditGuesser}
      show={EditGuesser}
      create={UsersCreate}
    />
    <Resource
      name="Orders"
      list={OrdersList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={OrderCreat}
    />
  </Admin>
);
