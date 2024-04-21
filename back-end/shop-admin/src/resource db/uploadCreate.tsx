import * as React from 'react';
import { Create, SimpleForm, TextInput, DateInput, required, ReferenceInput,ImageInput,ImageField } from 'react-admin';

export const uploadCreate = () => (
    <Create>
        <SimpleForm>
            <ImageInput source="picture" label="Product Image" accept="image/*">
                <ImageField source="src" title="title" />
            </ImageInput>
        </SimpleForm>
    </Create>
);