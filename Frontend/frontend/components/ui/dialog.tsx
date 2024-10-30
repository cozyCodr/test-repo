import React from "react";

interface DialogProps {
	open: boolean;
	onOpenChange: (open: boolean) => void;
	title: string;
	children: React.ReactNode;
}

export default function Dialog({
	open,
	onOpenChange,
	title,
	children,
}: DialogProps) {
	if (!open) return null;

	return (
		<div className="fixed inset-0 z-50 flex items-center justify-center">
			<div
				className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
				onClick={() => onOpenChange(false)}
			/>
			<div className="relative z-50 w-full max-w-2xl p-4 mx-4">
				<div className="relative bg-white rounded-lg shadow-xl">
					<div className="flex items-center justify-between p-4 border-b">
						<h2 className="text-lg font-semibold">{title}</h2>
						<button
							onClick={() => onOpenChange(false)}
							className="p-1 hover:bg-gray-100 rounded-full"
						>
							&#x2715;
						</button>
					</div>
					<div className="p-6">{children}</div>
				</div>
			</div>
		</div>
	);
}
