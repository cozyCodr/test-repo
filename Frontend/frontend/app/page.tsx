// components/ui/sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
	Home,
	Settings,
	Users,
	FileText,
	BarChart,
	HelpCircle,
} from "lucide-react";

const navigationItems = [
	{ name: "Dashboard", href: "/", icon: Home },
	{ name: "Key Concepts", href: "/key-concepts", icon: BarChart },
	{ name: "Upload Materials", href: "/documents", icon: FileText },
	{ name: "Quiz", href: "/team", icon: Users },
];

export default function Sidebar() {
	const pathname = usePathname();

	return (
		<aside className="fixed top-0 left-0 w-[300px] border-r min-h-screen bg-white">
			<div className="p-6">
				<div className="flex items-center gap-2 px-2 mb-8">
					<div className="w-8 h-8 bg-blue-600 rounded-lg" />
					<span className="text-xl font-semibold">EduQuery</span>
				</div>

				<nav className="space-y-1">
					{navigationItems.map((item) => {
						const isActive = pathname === item.href;
						const Icon = item.icon;

						return (
							<Link
								key={item.name}
								href={item.href}
								className={`
                  flex items-center gap-3 px-3 py-2 rounded-lg
                  transition-colors duration-200
                  ${
										isActive
											? "bg-blue-50 text-blue-600"
											: "text-gray-600 hover:bg-gray-50"
									}
                `}
							>
								<Icon size={20} />
								<span className="font-medium">{item.name}</span>
							</Link>
						);
					})}
				</nav>
			</div>

			<div className="absolute bottom-0 left-0 right-0 p-6">
				<div className="flex items-center gap-3 px-3 py-3 rounded-lg bg-gray-50">
					<div className="w-10 h-10 rounded-full bg-gray-200" />
					<div>
						<div className="font-medium">John Doe</div>
						<div className="text-sm text-gray-500">john@example.com</div>
					</div>
				</div>
			</div>
		</aside>
	);
}
