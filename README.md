
## API Reference

#### Get all items stored

```http
  GET /air_quality/store/api/data
```

#### Get item 

```http
  GET /air_quality/store/api/data/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get toxic gases 

```http
  GET /air_quality/api/data
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `latitude`      | `float` | **Required**. Site latitude |
| `longitude`      | `float` | **Required**. Site longitude |
| `type_gas`      | `string` | **Required**. Type of toxic gas |
| `forecast_days`      | `number` | **Required**. 16 < 0 days  |


#### Store toxic gases on database 

```http
  POST /air_quality/api/data
```

 **`Body params`**

```json
  {
      latitude : float
      longitude : float
      type_gas : string
      elevation : float
      forecast_days : number
      tag : string 
      data : list 
  }
```
