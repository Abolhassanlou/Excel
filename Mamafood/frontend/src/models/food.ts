export interface Food {
    id: number;
    food_name: string;
    description: string;
    restaurant_id: number;
    category_id: number;
    price: number;
    image_url: string;
    preparation_time: string;
}

export interface  FoodCategory {
    id: number;
    cat_name: string;
  }