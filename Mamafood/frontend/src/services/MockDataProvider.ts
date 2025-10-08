import { Food, FoodCategory } from "../models/food";


const mockFoodCategories: FoodCategory[] = [
  { id: 1, cat_name: "Vegetarisch" },
  { id: 2, cat_name: "Pasta" },
  { id: 3, cat_name: "Salate" },
  { id: 4, cat_name: "Bowls" },
  { id: 5, cat_name: "Reise" },
  { id: 6, cat_name: "Suppe" },
]

const mockFood : Food[] =[
    {
        id: 1,
        food_name: "Kuku Sabzi",
        description: "Vegetarisches Kräuteromelette",
        restaurant_id: 1,
        category_id: 1,
        price: 8.99,
        image_url: "/images/Kuku.png",
        preparation_time: "15 Minuten",
      },

      {
        id: 2,
        food_name: "Spaghetti Carbonara",
        description: "Original italienische Spaghetti mit Ei, Speck und Pecorino-Käse",
        restaurant_id: 1,
        category_id: 2, 
        price: 10.99,
        image_url: "/images/Pasta.png",
        preparation_time: "20 Minuten",
      },

      {
        id: 3,
        food_name: "Caesar Salad",
        description: "Frischer Salat mit Hähnchen, Croutons und Parmesan",
        restaurant_id: 2,
        category_id: 3, // Salat Kategorie
        price: 7.99,
        image_url: "/images/CaesarSalad.png",
        preparation_time: "10 Minuten",
      },
      {
        id: 4,
        food_name: "Falafel Bowl",
        description: "Frische Gemüse mit Falafel und  Hummus",
        restaurant_id: 3,
        category_id: 4, 
        price: 8.99,
        image_url: "/images/falafel.png",
        preparation_time: "10 Minuten",
      },

      {
        id: 5,
        food_name: "Maqlubaa",
        description: "Gekochter Reis mit gemischtem Gemüse und Fleisch",
        restaurant_id: 1,
        category_id: 2, 
        price: 7.49,
        image_url: "/images/Maqluba.png",
        preparation_time: "20 Minuten",
      },

      {
        id: 6,
        food_name: "Linsen Suppe",
        description: "Eine warme, cremige Linsen Suppe  mit frischen Kräutern",
        restaurant_id: 3,
        category_id: 3, 
        price: 5.99,
        image_url: "/images/linsensuppe.png",
        preparation_time: "10 Minuten",
      },
];

export const mockDataProvider = {
    getDishes: async () => Promise.resolve(mockFood),
    getDishById: async (id: number) => Promise.resolve(mockFood.find(d => d.id === id) || null),
    getCategories: async () => Promise.resolve(mockFoodCategories),
  };