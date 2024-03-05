import React, { createContext, useContext, useState } from 'react';

const SearchContext = createContext();

export const useSearch = () => useContext(SearchContext);

export const SearchProvider = ({ children }) => {
    const [searchPerformed, setSearchPerformed] = useState(false);
    const [searchCriteria, setSearchCriteria] = useState({ title: '', username: '' });

    return (
        <SearchContext.Provider value={{ searchPerformed, setSearchPerformed, searchCriteria, setSearchCriteria }}>
            {children}
        </SearchContext.Provider>
    );
};

