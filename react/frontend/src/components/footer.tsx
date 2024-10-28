interface FooterProps {
  project: string;
  name: string;
}

function Footer({ project, name }: FooterProps) {
  return (
    <footer className="footer footer-center bg-base-300 text-base-content p-4">
      <aside>
        <p>
          © {new Date().getFullYear()} - {project} made with love by {name} -
          All rights reserved.
        </p>
      </aside>
    </footer>
  );
}

export default Footer;
