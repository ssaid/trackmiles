import { FC, memo } from "react";


interface Props {
	label: string;
	content: number;
}

export const TimeBox: FC<Props> = memo(({label, content}) => {

	return (
		<div className="flex flex-col items-center mx-2">
			<span className="text-2xl font-bold">{ content }</span>
			<span className="text-lg">{ label }</span>
		</div>
	)
})
