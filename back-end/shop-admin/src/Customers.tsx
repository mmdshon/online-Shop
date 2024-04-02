import {
    CreateButton,
    Datagrid,
    FilterButton,
    FilterForm,
    ListBase,
    List,
    Pagination,
    TextField,
    TextInput,
    SearchInput,
    DeleteButton,
    ShowButton,
} from 'react-admin';
import { Stack } from '@mui/material';

const CustomerFilters = [
    <SearchInput source="name" alwaysOn />,
    <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
];
const ListToolbar = () => (
    <Stack direction="row" justifyContent="space-between">
        <FilterForm filters={CustomerFilters} />
        <div>
            <FilterButton filters={CustomerFilters} />
            <CreateButton />
        </div>
    </Stack>
)
export const CustomersList = () => (
    <List>
        <ListToolbar />
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="name" />
            <TextField source="email" />
            <TextField source="phone" />
            <DeleteButton label='delete'/>
            <ShowButton label='show'/>
        </Datagrid>
    </List>
);