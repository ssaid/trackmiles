import { useParams, useSearchParams } from "react-router-dom";


export const AnalyticsView = () => {

  const [searchParams] = useSearchParams();
  const origin = searchParams.get('origin');
  const dest = searchParams.get('dest');

  console.log({origin, dest})

  return (
    <div>
      <h1>Sabes quien soy? :)</h1>
      {
        JSON.stringify({origin, dest})
      }
    </div>
  )
}
