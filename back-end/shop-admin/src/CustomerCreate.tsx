import * as React from 'react';
import { Create, SimpleForm, TextInput, DateInput, required } from 'react-admin';

export const CustomerCreate = () => (
    <Create>
        <SimpleForm>
            <TextInput source="name" validate={[required()]} fullWidth />
            <TextInput source="phone" multiline={true} label="phone" />
            <TextInput source="email" multiline={true} label="email" />
        </SimpleForm>
    </Create>
);