interface MockupCodeProps {
  code: string;
}

function MockupCode({ code }: MockupCodeProps) {
  return (
    <div className="mockup-code w-6/12 m-auto">
      <pre data-prefix="$">
        <code>{code}</code>
      </pre>
    </div>
  );
}

export default MockupCode;
