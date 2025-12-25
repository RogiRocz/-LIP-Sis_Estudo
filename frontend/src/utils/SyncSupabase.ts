const syncArray = (currentArray: any[] | null, p: any) => {
	if (!currentArray) return []

	const { eventType, new: newItem, old: oldItem } = p

	if (eventType === 'INSERT') return [...currentArray, newItem]
	if (eventType === 'UPDATE') return currentArray.map((item) => (item.ID === newItem.ID ? newItem : item))
	if (eventType === 'DELETE') return currentArray.filter((item) => item.ID !== oldItem.ID)

	return currentArray
}

const syncMap = (currentMap: Map<number, any[]> | null, payload: any, parentKeyName: string) => {
    if (!currentMap) return new Map();
    const { eventType, new: newItem, old: oldItem } = payload;
    
    const parentId = eventType === 'DELETE' ? oldItem[parentKeyName] : newItem[parentKeyName];
    const list = currentMap.get(parentId) || [];
  
    let newList: any[];
    if (eventType === 'INSERT') newList = [...list, newItem];
    else if (eventType === 'UPDATE') newList = list.map(item => item.ID === newItem.ID ? newItem : item);
    else if (eventType === 'DELETE') newList = list.filter(item => item.ID !== oldItem.ID);
    else newList = list;
  
    currentMap.set(parentId, newList);
    return new Map(currentMap);
};

export {
    syncArray,
    syncMap
}